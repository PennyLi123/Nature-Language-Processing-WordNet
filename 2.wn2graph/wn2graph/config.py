from py2neo import Graph

# region Default values
# Graph database credentials
uri = "bolt://localhost:7687"
dbUser = "neo4j"
dbPass = "123"
dbName = "neo4j"
graph = Graph(uri, auth=(dbUser, dbPass), name=dbName)

# WordNet relations between senses and synsets stored in JSON files
# Key = JSON relation
# Index 0 = Changed relation name for neo4j
# Index 1 = Cost, used for weighted pathfinding
wn_relations = {
    "also": ["wn__also", 60],
    "antonym": ["wn__antonym", 90],
    "attribute": ["wn__attribute", 20],
    "causes": ["wn__causes", 40],
    "derivation": ["wn__derivation", 15],
    "domain_region": ["wn__domain_region", 65],
    "domain_topic": ["wn__domain_topic", 65],
    "entails": ["wn__entails", 50],
    "exemplifies": ["wn__exemplifies", 80],
    "has_domain_region": ["wn__has_domain_region", 65],
    "has_domain_topic": ["wn__has_domain_topic", 65],
    "holo_member": ["wn__holo_member", 65],
    "holo_part": ["wn__holo_part", 65],
    "holo_substance": ["wn__holo_substance", 65],
    "hypernym": ["wn__hypernym", 65],
    "hyponym": ["wn__hyponym", 65],
    "instance_hypernym": ["wn__instance_hypernym", 65],
    "instance_hyponym": ["wn__instance_hyponym", 65],
    "is_exemplified_by": ["wn__is_exemplified_by", 80],
    "mero_member": ["wn__mero_member", 65],
    "mero_part": ["wn__mero_part", 65],
    "mero_substance": ["wn__mero_substance", 65],
    "pertainym": ["wn__pertainym", 25],
    "participle": ["wn__participle", 25],
    "similar":[ "wn__similar", 20]}

# Lexical Relations
# Index 0 = Relation name for neo4j
# Index 1 = Cost, used for weighted pathfinding
rel_canForm = ["canonicalForm", 0]
rel_sense = ["sense", 0]
rel_lexSense = ["lexicalisedSense", 100]

# Lexical Node Lables
n_Form = "lex_Form"
n_Entry = "lex_Entry"
n_Sense = "lex_Sense"
n_Concept = "lex_Concept"

# PoS Nodes:
# Key = Node name in Neo4j
# Value = sysnet PoS
pos_nodes = {
    "Adjective": "a",
    "AdjectiveSatellite": "s",
    "Adverb": "r",
    "Verb": "v",
    "Noun": "n"
}

# PoS file names "data.pos.json"
file_pos = ["adj", "adv", "verb", "noun"]
# endregion