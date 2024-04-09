import inspect, time
from wn2graph import config
from config import graph


def IndexesConstraints():
    print(f"---\nStarting: {inspect.stack()[0][3]}")

    constraint_Concept = graph.run(f''' //Constraint for lexical Concepts to be unique
    CREATE CONSTRAINT con_{config.n_Concept}_id IF NOT EXISTS  FOR (s:{config.n_Concept}) REQUIRE (s.wn_id) IS UNIQUE''')

    index_Concept = graph.run(f''' //Index for Concepts on synset ID
    CREATE TEXT INDEX index_{config.n_Concept}_id IF NOT EXISTS FOR (s:{config.n_Concept}) on (s.wn_id)''')

    constraint_Senses = graph.run(f'''//Constraint for lexical Senses to be unique
    CREATE CONSTRAINT con_{config.n_Sense}_sense_key IF NOT EXISTS  FOR (l:{config.n_Sense}) REQUIRE (l.wn_sense_key) IS UNIQUE ''')

    index_Senses = graph.run(f''' //Index for Senses on sense_key
    CREATE TEXT INDEX index_{config.n_Sense}_sense_key IF NOT EXISTS FOR (l:{config.n_Sense}) on (l.wn_sense_key) ''')

    # Indexes and constraints for new nodes, OntoLex-Lemon
    index_Entry = graph.run(f''' //Index for Entry on lex_canonicalForm
    CREATE TEXT INDEX index_{config.n_Entry}_lex_canonicalForm IF NOT EXISTS FOR (l:{config.n_Entry}) on (l.lex_canonicalForm) ''')

    constraint_Form = graph.run(f''' //Unique constraint on lex_Form for lex_writtenForm
    CREATE CONSTRAINT con_{config.n_Form}_writtenForm IF NOT EXISTS FOR (f:{config.n_Form}) REQUIRE (f.lex_writtenForm) IS UNIQUE; ''')

    index_Form = graph.run(f''' //Index for Form on lex_writtenForm
    CREATE TEXT INDEX index_{config.n_Form}_lex_writtenForm IF NOT EXISTS FOR (l:{config.n_Form}) on (l.lex_writtenForm) ''')

    #################PROVISIONAL CHANGES TO HELP PROFORMANCE##########################

    # TODO: Change out (l:Adverb) to access pos_nodes dic instead
    con_pos_canonical = graph.run(f'''
    CREATE CONSTRAINT con_{config.n_Entry}_Adv_canonicalForm IF NOT EXISTS FOR (l:Adverb) REQUIRE (l.lex_canonicalForm) IS UNIQUE ''')

    con_pos_canonical = graph.run(f'''
    CREATE CONSTRAINT con_{config.n_Entry}_Adj_canonicalForm IF NOT EXISTS FOR (l:Adjective) REQUIRE (l.lex_canonicalForm) IS UNIQUE ''')

    con_pos_canonical = graph.run(f'''
    CREATE CONSTRAINT con_{config.n_Entry}_AdjSat_canonicalForm IF NOT EXISTS FOR (l:AdjectiveSatellite) REQUIRE (l.lex_canonicalForm) IS UNIQUE ''')

    con_pos_canonical = graph.run(f'''
    CREATE CONSTRAINT con_{config.n_Entry}_Verb_canonicalForm IF NOT EXISTS FOR (l:Verb) REQUIRE (l.lex_canonicalForm) IS UNIQUE ''')

    con_pos_canonical = graph.run(f'''
    CREATE CONSTRAINT con_{config.n_Entry}_Noun_canonicalForm IF NOT EXISTS FOR (l:Noun) REQUIRE (l.lex_canonicalForm) IS UNIQUE ''')

    print(f"Finished: {inspect.stack()[0][3]}\n---")

# TODO: ADD THIS BACK IN IF PERFORMANCE SUFFERS
#
# NOT CURRENTLY IMPLEMENTED
#
#def IndexsForRelations():
#     print(f"---\nStarting: {inspect.stack()[0][3]}")
#
#     for rel in config.relations:
#         indexs = graph.run(f'''
#             // Index REL {rel} on starting node
#             CREATE TEXT INDEX rel_{rel}_index IF NOT EXISTS FOR ()-[r:{rel}]-() on (r.src_id)
#             ''')
#
#     return print(f"Finished: {inspect.stack()[0][3]}\n---")

def InputData():
    print(f"---\nStarting: {inspect.stack()[0][3]}")
    for p in config.file_pos:
        cypher = graph.run(f'''
        // CREATE Synset + Lemmas
        // OMITTED old_keys, foreign, links, ili, gloss (null)

        WITH "file://data.{p}.json" AS path
            CALL apoc.load.json(path) yield value
            unwind value as data    
            unwind data.lemmas as lemmas
            MERGE (s:{config.n_Concept} {{wn_id: data.id}})
            ON CREATE SET s += {{wn_definition: data.definition,
                                wn_example: data.examples,
                                wn_pos: data.pos,
                                wn_subject: data.subject}}
            WITH s, data, lemmas
            MERGE (l:{config.n_Sense} {{wn_sense_key:lemmas.sense_key}})
            ON CREATE SET l += {{wn_lemma: lemmas.lemma,
                                wn_pos: data.pos,
                                wn_language: lemmas.language,
                                wn_forms: lemmas.forms,
                                wn_subcats: lemmas.subcats,
                                wn_importance: lemmas.importance}}
            MERGE (s)<-[r:{config.rel_lexSense[0]}]-(l)
            ON CREATE SET r+= {{cost:{config.rel_lexSense[1]}}}
            RETURN COUNT(r)
        ''')
        print(f"POS File: {p} OUTPUT: {cypher.data()}")

    return print(f"Finished: {inspect.stack()[0][3]}\n---")

# TODO: Add relfexives to relationships that currently do not have one (that need it)
def BuildRelationshipsWN():
    print(f"---\nStarting: {inspect.stack()[0][3]}")

    for wn_rel, rel_item in config.wn_relations.items():
        print(f"Relation without word pointers: {wn_rel}")
        rel_start = time.time()
        for p in config.file_pos:
            cypher = graph.run(f'''
            // Relationships ({wn_rel})

            CALL apoc.periodic.iterate('
                WITH "file://data.{p}.json" AS path
                CALL apoc.load.json(path) yield value
                unwind value as data
                unwind data.lemmas as lemmas
                unwind data.relations as relations
                WITH data.id as src_id,
                relations.rel_type as rel_type,
                relations.src_word as src_word,
                relations.trg_word as trg_word,
                relations.target as trg_id
                MATCH (s:{config.n_Concept}) WHERE s.wn_id = src_id AND rel_type = "{wn_rel}" AND src_word IS NULL
                MATCH (b:{config.n_Concept}) WHERE b.wn_id = trg_id AND trg_word IS NULL
                RETURN s, b, rel_type',
                'WITH s, b, rel_type
                MERGE (s)-[r:{rel_item[0]}]->(b)
                ON CREATE SET r += {{rel_type:"{rel_item[0]}",cost:{rel_item[1]}}}
                RETURN COUNT(r)', {{batchSize:100, parallel:false}})''')
            print(f"POS: {p} COUNT: {cypher.data()}")
        rel_end = time.time()
        print(f"Query time: {rel_end - rel_start}")



    for wn_rel, rel_item in config.wn_relations.items():
        print(f"Relation with word pointers: {wn_rel}")
        rel_start = time.time()
        for p in config.file_pos:
            cypher = graph.run(f'''
            // Relationships ({wn_rel})

            CALL apoc.periodic.iterate('
                WITH "file://data.{p}.json" AS path
                CALL apoc.load.json(path) yield value
                unwind value as data
                unwind data.lemmas as lemmas
                unwind data.relations as relations
                WITH data.id as src_id,
                relations.rel_type as rel_type,
                relations.src_word as src_word,
                relations.trg_word as trg_word,
                relations.target as trg_id
                MATCH (s:{config.n_Concept})<-[:{config.rel_lexSense[0]}]-(c:{config.n_Sense})
                WHERE s.wn_id = src_id AND rel_type = "{wn_rel}" AND c.wn_lemma = src_word
                MATCH (b:{config.n_Concept})<-[:{config.rel_lexSense[0]}]-(d:{config.n_Sense})
                WHERE b.wn_id = trg_id AND d.wn_lemma = trg_word
                RETURN c, d, rel_type, src_word, trg_word',
                'WITH c, d, rel_type, src_word, trg_word
                MERGE (c)<-[r:{rel_item[0]}]-(d)
                ON CREATE SET r += {{rel_type:"{rel_item[0]}",
                                    cost:{rel_item[1]}, 
                                    src_word:src_word,
                                    trg_word:trg_word}}
                RETURN COUNT(r)', {{batchSize:100, parallel:false}})''')
            print(f"POS: {p} COUNT: {cypher.data()}")
        rel_end = time.time()
        print(f"Query time: {rel_end - rel_start}")


    return print(f"Finished: {inspect.stack()[0][3]}\n---")

def BuildEntryToSense():
    print(f"---\nStarting: {inspect.stack()[0][3]}")
    for pos_node, pos in config.pos_nodes.items():
        print(f"Creating Nodes :{config.n_Entry}:{pos_node}")

        cypher = graph.run(f'''
            // Create node that links canonical form of Senses to canonical node
            MATCH (l:{config.n_Sense} {{wn_pos:"{pos}"}})
            WITH DISTINCT l.wn_lemma as dist_lemma, l.wn_pos as pos
            MERGE (e:{config.n_Entry}:{pos_node} {{lex_canonicalForm: dist_lemma, wn_pos: pos}})
            RETURN COUNT(e);
            ''')

        print(f"Finished creating OUTPUT:{cypher.data()}\n")
        print(f"Started linking nodes")

        cypher = graph.run(f'''
            // Linking the nodes together
            MATCH (e:{config.n_Entry}:{pos_node})
            MATCH (l:{config.n_Sense} {{wn_pos:"{pos}"}})
            WHERE e.lex_canonicalForm = l.wn_lemma AND e.wn_pos = l.wn_pos
            WITH e, l
            MERGE (e)-[r:{config.rel_sense[0]}]->(l)
                ON CREATE SET r.cost = {config.rel_sense[1]}
            RETURN COUNT(r)
            ''')

        print(f"Finished linking nodes OUTPUT:{cypher.data()}\n")
    print(f"Finished: {inspect.stack()[0][3]}\n---")

def BuildFormToEntry():
    print(f"---\nStarting: {inspect.stack()[0][3]}")

    print(f"Creating distinct {config.n_Entry} Nodes")
    cypher = graph.run(f'''
        // Creates distinct nodes from Entry's canonicalForms
        CALL apoc.periodic.iterate('
        MATCH (e:{config.n_Entry})
        WITH DISTINCT e.lex_canonicalForm as writtenForm
        RETURN writtenForm','WITH writtenForm     
        MERGE (f:{config.n_Form} {{lex_writtenForm: writtenForm}})',
        {{batchSize:100, parallel:True}})
        ''')
    print(f"OUTPUT:{cypher.data()}\nFinished creating")

    print(f"Linking {config.n_Form} to {config.n_Entry}")
    cypher = graph.run(f'''
        // Links the Form nodes to Entry nodes
        CALL apoc.periodic.iterate('
        MATCH (e:{config.n_Entry})
        MATCH (f:{config.n_Form})
        WHERE e.lex_canonicalForm = f.lex_writtenForm
        RETURN e, f','
        WITH e, f
        MERGE (f)-[r:{config.rel_canForm[0]}]->(e)
            ON CREATE SET r.cost = {config.rel_canForm[1]}',
        {{batchSize:100, parallel:False}})
        ''')
    print(f"OUTPUT:{cypher.data()}\nFinished linking")
    print(f"Finished: {inspect.stack()[0][3]}\n---")

def checkFiles():
    for pos in config.file_pos:
        cypher = graph.run(f'''
            // Checking if files are imported by running query
            WITH "file://data.{pos}.json" AS path
            CALL apoc.load.json(path) yield value
            unwind keys(value) as key
            RETURN key, apoc.meta.type(value[key]) limit 12
            ''')

    return print("All files are imported and accesible\n---<Setting up graph>---")

def main():
    try:
        checkFiles()
        try:
            start = time.time()
            IndexesConstraints()
            InputData()
            BuildRelationshipsWN()
            BuildEntryToSense()
            BuildFormToEntry()
            end = time.time()
            print(f"Finished in: {end - start}")
        except:
            print("Unabled to setup up graph.")
    except:
        print("Cannot find or missing imported files, check folder laction")

if __name__ == "__main__":
    main()