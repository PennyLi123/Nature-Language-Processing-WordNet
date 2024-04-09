# Nature-Language-Processing-WordNet

# Project Overview
A Study of Text Similarity Methods using Natural Language Processing Tool (NLTK) with Wordnet (lexical database), which is modelled into Neo4j(graphic database) for querying and traversing. Additionally, a web application was developed to allow users to interactively query and explore semantic similarity values between English words.

# Problem
Semantic similarity analysis plays a crucial role in various fields such as data processing, linguistics, and artificial intelligence. However, accurately measuring semantic similarity between concepts poses challenges, particularly when dealing with large lexical databases like WordNet. Traditional literature-based methods may not fully exploit the rich semantic relationships within WordNet. Moreover, there is often a lack of integration between different similarity measures and data formats in some systems, which may impede comprehensive comparisons and evaluations.

# Tools used
* Database: WordNet lexical database 
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Fragment%20of%20WordNet%20concept%20in%20taxonomy.png" width="430">


* Nature Language Tool-Kit (NLTK): WordNet Corpus, Semantic Similarity Package

* Neo4j: Graphic database(for WordNet modelling), Graph Data Sience Library(for WordNet data query and traversal), Cypher query languge
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Example%20Blocks%20of%20Property%20Graph.png" width="100" height="250">

* Flask: Python web application framework, WTForms(pass data from the front-end to the back-end)

# System Architecture
- The system is split into three main parts, pulling data, loading data, and the interface. 
- The solid blocks in the Figure below cover the similarity methods run against NLTK data, while the dashed block shows the process of similarity methods run against Neo4j. 
- This involves downloading the NLTK data from its website and creating a new SimilarityMethods.py file to call the algorithm in the nltk corpus reader module and the nltk data package, to compute the results for the data received in forms.py, and then to supplement the app.py file with the NLTK algorithms to handle the data received from forms and the results returned from similarityMethods.py, then finally the app.py file passes all the results to the web page to display their results in a table.
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/System%20Architecture.png" width="430">

# Action
## 1.Modeling WordNet into Neo4j
To address these challenges, this project undertook the modeling of the WordNet lexical database into a Neo4j graph database.
Used a created module called wn2graph using Python 3.9
* Pulling data
Using the wn2graph module pullData.py uses the library regex to search for IDs and POS with pattern search and requests for connecting to the WordNet RDF webpage to download the data to be used for loading. The retrieved data is then stored in a "data.pos.json"file.
More details see attachment: 
[2.wn2graph](https://github.com/PennyLi123/Nature-Language-Processing-WordNet/tree/main/2.wn2graph)

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Basic%20model%20of%20pullData.png" width="430">
Basic model of pullData.py

* Loading and modelling
Use the python library Py2neo for this section, which serves as the bridge between Python and Neo4j Server 4.4.7, allowing us to run queries on the graph. Import a config.py file, which stores frequently used variables for graph queries and the graph credentials that connect to the graph.

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Basic%20model%20of%20setupGraph.png" width="430">
Basic model of setupGraph.py

## 2.Neo4j Similarity Analysis
This involved the transformation of WordNet's intricate semantic relations into a structured graph representation, facilitating efficient storage and traversal. 

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Lexical%20structure%20model%20of%20Wordnet%20Graph.png" width="430">

For example, the graph model in Neo4j for word 'open'is shown below. Node with light purple colour indicates 'open' as simplest written form without meaning. Nodes with red, blue, green colour on the left of the purple written form indicate the POS(part of speech) of word 'open' are noun, adjective and adjective satellite respectively. Pink node on the right side of the purple written form indicates 'open' as verb. Then a ralation "sense" with direction start from "lex_Entry"(pink verb node) to "lex_Sense"(red node on the right side), and another relation "lexicalised Sense" with direction start from "lex_sense"(red node) to "lex_concept"(nude node). 

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Example%20of%20graph%20model%20in%20Neo4j.png" width="430">

- Path similarity Cypher Query in Neo4j
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Path%20similarity%20Cypher%20Query%20in%20Neo4j.png" width="430">

- Example of shortest path from blue nodes “Sense” to “Sense”in Neo4j
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/shortest%20path%20from%20“Sense”%20to%20“Sense”in%20Neo4j.png" width="430">

- Results of path similarity in Neo4j
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Results%20of%20path%20similarity%20in%20Neo4j.png" width="430">

## 3.Install NLTK library and download WordNet corpus
Created a new python3.8 notebook using the Jupiter Notebook web application that launched by Anaconda Navigator to install NLTK library and WordNet corpus. 
## 4.Similarity analysis with NLTK WordNet corpuse data
With NLTK WordNet corpus data downloaded, utilized WordNet::similarity Package in NLTK performed WordNet similarity analysis. Six similarity algorithms are implemented: Lch similarity, Wup similarity, Information-based Measures, Lin Similarity, Resnik similarity, Jcn Similarity.

## Flask Interface
- Developed a web interface to allow users to interactively query and explore semantic similarity values between English words and enables users to apply different similarity methods and compare results.
- As the user inputs the source word and target word and sends a run query request, the results of both neo4j and nltk will be displayed in a table together for a visual cross-sectional comparison.

- Web page of word to word sim function

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/web%20page%20of%20word%20to%20word%20sim%20function.png" width="430">

- Table displaying results of nltk and neo4j methods

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Table%20displaying%20results%20of%20nltk%20and%20neo4j%20methods.png" width="430">

# Results
- Summary results of each measures for Noun

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Summary%20results%20of%20each%20measures%20for%20Noun.png" width="430">

In conclusion, the comparison revealed that NLTK's path-based similarity values are more accurate than neo4j's due to differences in their graph models and is-a hierarchies. The Resnik and Lin methods are ineffective for distant concept pairs with root node lcs, yielding 0 values. Jcn and Lin methods, utilizing ic values, prove more accurate for similarity measurement.
