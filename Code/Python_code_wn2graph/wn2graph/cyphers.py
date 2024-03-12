import inspect
from wn2graph import config
from wn2graph.config import graph


"""

Queries to run against the graph databse, to find similarity

"""

def distinctRelationfrom():
    list = []
    for pos in config.file_pos:
        cypher = graph.run(f'''     
        // Distinct relations for each pos
        WITH "file://data.{pos}.json" AS path
            CALL apoc.load.json(path) yield value
            unwind value as data
            unwind data.relations as relations
            RETURN distinct relations.rel_type
        ''')
        for x in cypher.data():
            for key, value in x.items():
                if value not in list:
                    list.append(value)

    return print(f"Number of relations: {len(list)}\n{list}")


def distinctSynsetsfrom():
    list = []
    for pos in config.file_pos:
        cypher = graph.run(f'''     
        // Distinct relations for each pos
        WITH "file://data.{pos}.json" AS path
            CALL apoc.load.json(path) yield value
            unwind value as data
            unwind data.id as id
            RETURN distinct id
        ''')
        for x in cypher.data():
            for key, value in x.items():
                if value not in list:
                    list.append(value)

    return print(f"Number of Synsets: {len(list)}")

def countUniqueSenses():
    list = []
    for pos in config.file_pos:
        cypher = graph.run(f'''     
        // Distinct relations for each pos
        WITH "file://data.{pos}.json" AS path
            CALL apoc.load.json(path) yield value
            unwind value as data
            unwind data.lemmas as lemmas
            RETURN lemmas.lemma
        ''')
        for x in cypher.data():
            for key, value in x.items():
                list.append(value)


    return print(f"Number of Synsets: {len(list)}")



def count4eachRelation():

    for relKey, relValue in config.wn_relations.items():
        cypher = graph.run(f'''
                MATCH ()-[r:{relValue[0]}]-()
                RETURN COUNT(r)
            ''')
        print(f"{relValue[0]}: {cypher.data()}")

    cypher = graph.run(f'''
                    MATCH ()-[r:{config.rel_canForm[0]}]-()
                    RETURN COUNT(r)
                ''')
    print(f"{config.rel_canForm[0]}: {cypher.data()}")

    cypher = graph.run(f'''
                    MATCH ()-[r:{config.rel_sense[0]}]-()
                    RETURN COUNT(r)
                ''')
    print(f"{config.rel_sense[0]}: {cypher.data()}")

    cypher = graph.run(f'''
                    MATCH ()-[r:{config.rel_lexSense[0]}]-()
                    RETURN COUNT(r)
                ''')
    print(f"{config.rel_lexSense[0]}: {cypher.data()}")



def setCostsOnRels():

    print(f"---\nStarting: {inspect.stack()[0][3]}")

    for relKey, relValue in config.wn_relations.items():
        cypher = graph.run(f'''
            MATCH ()-[r:{relValue[0]}]-()
            SET r.cost = {relValue[1]}
            RETURN r.cost limit 1
        ''')
        print(f"{relValue[0]}\n{relValue[1]}")

    cypher = graph.run(f'''
                MATCH ()-[r:{config.rel_canForm[0]}]-()
                SET r.cost = {config.rel_canForm[1]}
                RETURN r.cost limit 1
            ''')

    cypher = graph.run(f'''
                    MATCH ()-[r:{config.rel_sense[0]}]-()
                    SET r.cost = {config.rel_sense[1]}
                    RETURN r.cost limit 1
                ''')

    cypher = graph.run(f'''
                    MATCH ()-[r:{config.rel_lexSense[0]}]-()
                    SET r.cost = {config.rel_lexSense[1]}
                    RETURN r.cost limit 1
                ''')

def shortestPathFormNodes(start, end):

    cypher = graph.run(f'''
        MATCH p=shortestPath((l:{config.n_Form} {{lex_writtenForm:"{start}"}})-[*]-(b:lex_Form {{lex_writtenForm:"{end}"}}))
        UNWIND relationships(p) as rels
        RETURN COUNT(rels) - 4 AS numRels, p
        ''')

    output = cypher.data()[0]
    print(output["numRels"])
    print(output)
    print(output["p"])


def testConnection():
    cypher = graph.run("""
        MATCH (n) WHERE id(n) = 1
        RETURN n = n
        """)
    return cypher.data()

def checkExsistsGDSgraph():

    cypherCheck = graph.run("""
            CALL gds.graph.list()
        """)

    if cypherCheck.data() == []:
        print("GDS projected graph not created, creating one now.")
        cypher = graph.run('''
                // Create projected graph for GDS
                CALL gds.graph.project.cypher(
                    'all','
                    MATCH (n)
                    RETURN id(n) as id',
                    'MATCH (n)-[r]-(m)
                    RETURN id(n) as source, id(m) as target, type(r) as type, r.cost as cost')
                    YIELD graphName as graph, nodeCount AS nodes, relationshipCount AS rels
                ''')
        return cypher.data()

    return True





def word2word(source, target):

    print(source, target)

    cypher = graph.run(f'''
        // V2 of Similarities Word2Word

        MATCH (n:lex_Form {{lex_writtenForm:"{source}"}})-[:canonicalForm]->(npos:lex_Entry)
        MATCH (t:lex_Form {{lex_writtenForm:"{target}"}})-[:canonicalForm]->(tpos:lex_Entry)
        
        MATCH shortP=shortestpath((n)-[*0..20]-(t))
        
        CALL gds.shortestPath.dijkstra.stream("all", {{
            sourceNode: n,
            targetNode: t,
            relationshipWeightProperty: "cost"
        }}) YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path as dijkstraPath
        unwind costs as costsU
        RETURN
            n.lex_writtenForm as Source,
            npos.wn_pos as sPOS,
            t.lex_writtenForm as Target,
            tpos.wn_pos as tPOS,
            round((length(shortP)-4), 5) as shortestPathLen,
            round((1.0/(1+length(shortP)-4)), 5) as shortestPathSim,
            (length(dijkstraPath)-4) as dijkstraPathLen,
            (totalCost) as dijkstraTotalCost,
            round(avg(costsU), 5)  as dijkstraAvgCost,
            round((1.0/(1+length(dijkstraPath)-4)), 5) as dijkstraPathSim,
            costs
        ''')
    return cypher.data()

def word2connects(source):

    print(source)

    cypher = graph.run(f'''
        // V2 Direct links to Word from Sense

        MATCH p1=(n:lex_Form {{lex_writtenForm:"{source}"}})-[:canonicalForm]->(npos:lex_Entry)-[:sense]->(:lex_Sense)-[:lexicalisedSense]->
        (c:lex_Concept)<-[:lexicalisedSense]-(:lex_Sense)<-[:sense]-(tpos:lex_Entry)<-[:canonicalForm]-(t:lex_Form)
        
        MATCH shortP=shortestpath((n)-[*0..10]-(t))
        
        CALL gds.shortestPath.dijkstra.stream("all", {{
            sourceNode: n,
            targetNode: t,
            relationshipWeightProperty: "cost"
        }}) YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path as dijkstraPath
        unwind costs as costsU
        RETURN
            n.lex_writtenForm as Source,
            npos.wn_pos as sPOS,
            c.wn_definition as SharedConcept,
            t.lex_writtenForm as Target,
            tpos.wn_pos as tPOS,
            round((length(shortP)-4), 5) as shortestPathLen,
            round((1.0/(1+length(shortP)-4)), 5) as shortestPathSim,
            (length(dijkstraPath)-4) as dijkstraPathLen,
            (totalCost) as dijkstraTotalCost,
            round(avg(costsU), 5)  as dijkstraAvgCost,
            round((1.0/(1+length(dijkstraPath)-4)), 5) as dijkstraPathSim,
            costs
        ''')

    return cypher.data()

def wordsFromRelatedConcepts(source):
    print(source)

    cypher = graph.run(f'''
            // v3 Words which have a relation to source Word's concept
            
            MATCH p1=(n1:lex_Form {{lex_writtenForm:"{source}"}})-[:canonicalForm]->(npos:lex_Entry)-[:sense]->(n2:lex_Sense)-[:lexicalisedSense]->(c:lex_Concept)-[*1..1]-(m:lex_Concept)
            MATCH p2=(m:lex_Concept)<-[:lexicalisedSense]-(t2:lex_Sense)<-[:sense]-(tpos:lex_Entry)<-[:canonicalForm]-(t1:lex_Form) WHERE t1.lex_writtenForm <> n1.lex_writtenForm
            
            MATCH shortP=shortestpath((n1)-[*0..10]-(t1))
            
            
            CALL gds.shortestPath.dijkstra.stream("all", {{
                sourceNode: n1,
                targetNode: t1,
                relationshipWeightProperty: "cost"
            }}) YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path as dijkstraPath
            unwind costs as costsU
            RETURN 
                n1.lex_writtenForm as Source,
                npos.wn_pos as sPOS,
                t1.lex_writtenForm as Target,
                tpos.wn_pos as tPOS,
                round((length(shortP)-4), 5) as shortestPathLen,
                round((1.0/(1+length(shortP)-4)), 5) as shortestPathSim,
                (length(dijkstraPath)-4) as dijkstraPathLen,
                (totalCost) as dijkstraTotalCost,
                round(avg(costsU), 5)  as dijkstraAvgCost,
                round((1.0/(1+length(dijkstraPath)-4)), 5) as dijkstraPathSim,
                costs
                ORDER BY n1.lex_writtenForm DESC
            ''')

    return cypher.data()

def w2wjacard(source, target):
    cypher = graph.run(f"""
        MATCH (n:lex_Sense {{wn_lemma: "{source}"}})
        MATCH (t:lex_Sense {{wn_lemma: "{target}"}})
        CALL apoc.path.expand(n, null, "lex_Sense|lex_Concept", 0, 1) yield path as pathN
        CALL apoc.path.expand(t, null, "lex_Sense|lex_Concept", 0, 1) yield path as pathT
        unwind nodes(pathN) as nNodes
        unwind nodes(pathT) as tNodes
        with collect(id(nNodes)) as col_nNodes,
            collect(id(tNodes)) as col_tNodes
        RETURN "{source}" as sourceNode, "{target}" as targetNode,
                gds.similarity.jaccard(col_nNodes, col_tNodes) as gdsJaccardSimilarity,
                gds.similarity.overlap(col_nNodes, col_tNodes) as gdsOverlapSimilarity,
                gds.similarity.cosine(col_nNodes, col_tNodes) as gdsCosineSimilarity,
                gds.similarity.pearson(col_nNodes, col_tNodes) as gdsPearsonSimilarity,
                gds.similarity.euclideanDistance(col_nNodes, col_tNodes) as gdsEuclideanDistanceSimilarity,
                gds.similarity.euclidean(col_nNodes, col_tNodes) as gdsEuclideanSimilarity
        """)

    return cypher.data()


