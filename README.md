# Nature-Language-Processing-WordNet

# Project Overview
A Study of Text Similarity Methods using 𝑵𝒂𝒕𝒖𝒓𝒂𝒍 𝑳𝒂𝒏𝒈𝒖𝒂𝒈𝒆 𝑷𝒓𝒐𝒄𝒆𝒔𝒔𝒊𝒏𝒈 𝑻𝒐𝒐𝒍 `𝑵𝑳𝑻𝑲` with `𝑾𝒐𝒓𝒅𝑵𝒆𝒕` 𝒍𝒂𝒓𝒈𝒆 𝒍𝒆𝒙𝒊𝒄𝒂𝒍 𝒅𝒂𝒕𝒂𝒃𝒂𝒔𝒆, which is modelled into `𝑵𝒆𝒐4𝒋` 𝒈𝒓𝒂𝒑𝒉𝒊𝒄 𝒅𝒂𝒕𝒂𝒃𝒂𝒔𝒆 for querying and traversing. Additionally, a 𝑾𝒆𝒃 𝑨𝒑𝒑𝒍𝒊𝒄𝒂𝒕𝒊𝒐𝒏 was developed to allow users to interactively query and explore 𝒔𝒆𝒎𝒂𝒏𝒕𝒊𝒄 𝒔𝒊𝒎𝒊𝒍𝒂𝒓𝒊𝒕𝒚 𝒗𝒂𝒍𝒖𝒆𝒔 between English words.

# Problem
𝑺𝒆𝒎𝒂𝒏𝒕𝒊𝒄 𝒔𝒊𝒎𝒊𝒍𝒂𝒓𝒊𝒕𝒚 𝒂𝒏𝒂𝒍𝒚𝒔𝒊𝒔 plays a crucial role in various fields such as 𝒅𝒂𝒕𝒂 𝒑𝒓𝒐𝒄𝒆𝒔𝒔𝒊𝒏𝒈, 𝒍𝒊𝒏𝒈𝒖𝒊𝒔𝒕𝒊𝒄𝒔, 𝒂𝒏𝒅 𝒂𝒓𝒕𝒊𝒇𝒊𝒄𝒊𝒂𝒍 𝒊𝒏𝒕𝒆𝒍𝒍𝒊𝒈𝒆𝒏𝒄𝒆 (𝑨𝑰). However, accurately measuring semantic similarity between concepts poses challenges, particularly when dealing with large lexical database like `𝑾𝒐𝒓𝒅𝑵𝒆𝒕`. Traditional literature-based methods may not fully exploit the rich semantic relationships within WordNet. Moreover, there is often a lack of integration between different similarity measures and data formats in some systems, which may impede 𝒄𝒐𝒎𝒑𝒓𝒆𝒉𝒆𝒏𝒔𝒊𝒗𝒆 𝒄𝒐𝒎𝒑𝒂𝒓𝒊𝒔𝒐𝒏𝒔 and 𝒆𝒗𝒂𝒍𝒖𝒂𝒕𝒊𝒐𝒏𝒔. 

# Tools used
* Database: `WordNet` lexical database 
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Fragment%20of%20WordNet%20concept%20in%20taxonomy.png" width="430">


* Nature Language Tool-Kit `NLTK`: WordNet Corpus, Semantic Similarity Package

* `Neo4j`: Graphic database(for WordNet modelling), Graph Data Sience Library(for WordNet data query and traversal), Cypher query languge
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Example%20Blocks%20of%20Property%20Graph.png" width="300" height="390">

* `Flask`: `Python` web application framework, `WTForms`(pass data from the front-end to the back-end)

# System Architecture
- The system is split into three main parts, 𝒑𝒖𝒍𝒍𝒊𝒏𝒈 𝒅𝒂𝒕𝒂, 𝒍𝒐𝒂𝒅𝒊𝒏𝒈 𝒅𝒂𝒕𝒂, and the 𝒊𝒏𝒕𝒆𝒓𝒇𝒂𝒄𝒆.
- The solid blocks in the Figure below cover the 𝒔𝒊𝒎𝒊𝒍𝒂𝒓𝒊𝒕𝒚 𝒎𝒆𝒕𝒉𝒐𝒅𝒔 run against `NLTK data`, while the dashed block shows the process of 𝒔𝒊𝒎𝒊𝒍𝒂𝒓𝒊𝒕𝒚 𝒎𝒆𝒕𝒉𝒐𝒅𝒔 run against `Neo4j`. 
- This involves downloading the `NLTK data` from its website and creating a new `SimilarityMethods.py` file to call the algorithm in the `nltk corpus reader` module and the `nltk data` package, to compute the results for the data received in `forms.py`, and then to supplement the `app.py` file with the 𝑵𝑳𝑻𝑲 𝒂𝒍𝒈𝒐𝒓𝒊𝒕𝒉𝒎𝒔 to handle the data received from forms and the results returned from `similarityMethods.py`, then finally the `app.py` file passes all the results to the 𝒘𝒆𝒃 𝒑𝒂𝒈𝒆 to display their results in a table.
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/System%20Architecture.png" width="430">

# Action
## 1.Modeling WordNet into Neo4j
To address these challenges, this project undertook the modeling of the `WordNet` lexical database into a `Neo4j` graph database.
Used a created module called `wn2graph` using `Python 3.9`

### Basic model of pullData.py
* Pulling data
Using the `wn2graph` module `pullData.py` uses the library regex to search for IDs and POS with pattern search and requests for connecting to the WordNet RDF webpage to download the data to be used for loading. The retrieved data is then stored in a `"data.pos.json"`file.
More details see attachment: 
[2.wn2graph](https://github.com/PennyLi123/Nature-Language-Processing-WordNet/tree/main/2.wn2graph)

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Basic%20model%20of%20pullData.png" width="430">

### Basic model of setupGraph.py
* Loading and modelling
Use the python library `Py2neo` for this section, which serves as the bridge between `Python` and `Neo4j Server 4.4.7`, allowing us to run queries on the graph. Import a `config.py` file, which stores frequently used variables for graph queries and the graph credentials that connect to the graph.

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Basic%20model%20of%20setupGraph.png" width="430">


## 2.Neo4j Similarity Analysis
This involved the transformation of WordNet's intricate semantic relations into a structured graph representation, facilitating efficient storage and traversal. 

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Lexical%20structure%20model%20of%20Wordnet%20Graph.png" width="630">

For example, the graph model in `Neo4j` for word 'open'is shown below. 

𝑵𝒐𝒅𝒆 with 𝒍𝒊𝒈𝒉𝒕 𝒑𝒖𝒓𝒑𝒍𝒆 colour indicates '𝒐𝒑𝒆𝒏' as 𝒔𝒊𝒎𝒑𝒍𝒆𝒔𝒕 𝒘𝒓𝒊𝒕𝒕𝒆𝒏 𝒇𝒐𝒓𝒎 𝒘𝒊𝒕𝒉𝒐𝒖𝒕 𝒎𝒆𝒂𝒏𝒊𝒏𝒈. 

𝑵𝒐𝒅𝒆𝒔 with 𝒓𝒆𝒅, 𝒃𝒍𝒖𝒆, 𝒈𝒓𝒆𝒆𝒏 colour on the left of the purple written form indicate the POS(part of speech) of word '𝒐𝒑𝒆𝒏' are 𝒏𝒐𝒖𝒏, 𝒂𝒅𝒋𝒆𝒄𝒕𝒊𝒗𝒆 𝒂𝒏𝒅 𝒂𝒅𝒋𝒆𝒄𝒕𝒊𝒗𝒆 𝒔𝒂𝒕𝒆𝒍𝒍𝒊𝒕𝒆 respectively. 

𝑷𝒊𝒏𝒌 𝒏𝒐𝒅𝒆 on the right side of the purple written form indicates '𝒐𝒑𝒆𝒏' as 𝒗𝒆𝒓𝒃. 

Then a ralation "sense" with direction start from "lex_Entry"(pink verb node) to "lex_Sense"(red node on the right side), and another relation "lexicalised Sense" with direction start from "lex_sense"(red node) to "lex_concept"(nude node). 

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Example%20of%20graph%20model%20in%20Neo4j.png" width="630">

- Path similarity Cypher Query in Neo4j
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Path%20similarity%20Cypher%20Query%20in%20Neo4j.png" width="290">

- Example of shortest path from blue nodes “Sense” to “Sense”in Neo4j
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/shortest%20path%20from%20“Sense”%20to%20“Sense”in%20Neo4j.png" width="630">

- Results of path similarity in Neo4j
<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Results%20of%20path%20similarity%20in%20Neo4j.png" width="430">

## 3.Install NLTK library and download WordNet corpus
Created a new python3.8 notebook using the Jupiter Notebook web application that launched by Anaconda Navigator to install NLTK library and WordNet corpus. 

## 4.Similarity analysis with NLTK WordNet corpuse data

With NLTK WordNet corpus data downloaded, utilized WordNet::similarity Package in NLTK performed WordNet similarity analysis. 

Six similarity algorithms are implemented: Lch similarity, Wup similarity, Information-based Measures, Lin Similarity, Resnik similarity, Jcn Similarity.

## Flask Interface
- Developed a web interface to allow users to interactively query and explore semantic similarity values between English words and enables users to apply different similarity methods and compare results.
- As the user inputs the source word and target word and sends a run query request, the results of both neo4j and nltk will be displayed in a table together for a visual cross-sectional comparison.

- Web page of word to word sim function

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/web%20page%20of%20word%20to%20word%20sim%20function.png" width="430">

- Table displaying results of nltk and neo4j methods

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Table%20displaying%20results%20of%20nltk%20and%20neo4j%20methods.png" width="730">

# Results
- Summary results of each measures for Noun

<img src="https://github.com/PennyLi123/Nature-Language-Processing-WordNet/blob/main/3.Screenshots/Summary%20results%20of%20each%20measures%20for%20Noun.png" width="630">

In conclusion, the comparison revealed that NLTK's path-based similarity values are more accurate than Neo4j's due to differences in their graph models and is-a hierarchies. The Resnik and Lin methods are ineffective for distant concept pairs with root node lcs, yielding 0 values. Jcn and Lin methods, utilizing ic values, prove more accurate for similarity measurement.
