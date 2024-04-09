from flask import Flask
from flask import render_template, request
from wn2graph import cyphers
from forms import word2input, word1inputs
from SimilaryMethods import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '2c8553196a4dafa672b8c68d70a24e21eedb937d'

@app.route('/')
def hello_world():  # put application's code here
    return home()

@app.route("/home/", methods=['GET', 'POST'])
def home(): # home landing page
    return render_template("home.html")

@app.route("/w2word/", methods=['GET', 'POST'])
def w2word():
    print("w2word()")
    form = word2input(request.form)

    if request.method == 'POST' and form.validate():
        wordN = form.word1.data
        wordT = form.word2.data
        try:
            print(f"GDS projected graph created: {cyphers.checkExsistsGDSgraph()}")
            cypherOut = cyphers.word2word(wordN, wordT)
            print(cypherOut)
            return render_template("w2word.html", w2word_form=form, cypherOut=cypherOut)
        except:
            return render_template("w2word.html", w2word_form=form)


    print("Using default values for query")

    wordN = "open"
    wordT = "close"
    print(f"GDS projected graph created: {cyphers.checkExsistsGDSgraph()}")
    cypherOut = cyphers.word2word(wordN, wordT)
    print(cypherOut)
    return render_template("w2word.html", w2word_form=form, cypherOut=cypherOut)

@app.route("/w2synonym/", methods=['GET', 'POST'])
def w2synonym():
    errorInput = "<h2>Error with input, either input is not in the graph, or input is not lowercase"
    form = word1inputs(request.form)

    if request.method == 'POST' and form.validate():
        wordN = form.word1.data
        try:
            print(f"GDS projected graph created: {cyphers.checkExsistsGDSgraph()}")
            cypherOut = cyphers.word2connects(wordN)
            print(cypherOut)
            return render_template("w2synonym.html", form=form, cypherOut=cypherOut)
        except:
            return render_template("w2synonym.html", form=form)

    print("Using default values for query")

    wordN = "open"
    print(f"GDS projected graph created: {cyphers.checkExsistsGDSgraph()}")
    cypherOut = cyphers.word2connects(wordN)
    print(cypherOut)
    return render_template("w2synonym.html", form=form, cypherOut=cypherOut)

@app.route("/w2concept2w/", methods=['GET', 'POST'])
def w2concept2w():
    form = word1inputs(request.form)

    if request.method == 'POST' and form.validate():
        wordN = form.word1.data
        try:
            print(f"GDS projected graph created: {cyphers.checkExsistsGDSgraph()}")
            cypherOut = cyphers.wordsFromRelatedConcepts(wordN)
            print(cypherOut)
            return render_template("w2concept2w.html", form=form, cypherOut=cypherOut)
        except:
            return render_template("w2concept2w.html", form=form)

    print("Using default values for query")

    wordN = "open"
    print(f"GDS projected graph created: {cyphers.checkExsistsGDSgraph()}")
    cypherOut = cyphers.wordsFromRelatedConcepts(wordN)
    print(cypherOut)
    return render_template("w2concept2w.html", form=form, cypherOut=cypherOut)


@app.route("/w2w_gds/", methods=['GET', 'POST'])
def w2w_gds(): # home landing page
    print("w2w_gds()")
    form = word2input(request.form)

    if request.method == 'POST' and form.validate():
        wordN = form.word1.data
        wordT = form.word2.data
        try:
            print(f"GDS projected graph created: {cyphers.checkExsistsGDSgraph()}")
            cypherOut = cyphers.w2wjacard(wordN, wordT)
            print(cypherOut)
            return render_template("w2w_gds.html", w2word_form=form, cypherOut=cypherOut)
        except:
            return render_template("w2w_gds.html", w2word_form=form)

    print("Using default values for query")

    wordN = "open"
    wordT = "open up"
    print(f"GDS projected graph created: {cyphers.checkExsistsGDSgraph()}")
    cypherOut = cyphers.w2wjacard(wordN, wordT)
    print(cypherOut)
    return render_template("w2w_gds.html", w2word_form=form, cypherOut=cypherOut)


@app.route("/w2w_sim/", methods=['GET', 'POST'])
def w2w_sim():
    print("Similar method")
    # get the form requested
    form = word2input(request.form)

    # request validate
    if request.method == 'POST' and form.validate():
        wordN = form.word1.data
        wordT = form.word2.data
        try:
            print(f"GDS projected graph created: {cyphers.checkExsistsGDSgraph()}")
            # get the results returned from similarityMethods.py
            pathSimilarityScore = pathSimilar(wordN, wordT)
            resSimilarityScore = resSimilar(wordN, wordT)

            lchScore = lchSimilar(wordN, wordT)
            wupScore = wupSimilar(wordN, wordT)
            jcnScore = jcnSimilar(wordN, wordT)

            # print all the similarity results
            print(f"lch score: {lchScore:.2f}, wup score: {wupScore:.2f},path similar score: {pathSimilarityScore:.2f}, res similar score: {resSimilarityScore:.2f},")

            ##information content measure method
            lin_measurement_score = linMeasure(wordN, wordT)
            print("Lin's measure: {:.2f}".format(lin_measurement_score))

            # Create a dictionary to gather the results printed
            cypherDict = {}
            cypherDict["sourceNode"] = wordN
            cypherDict["targetNode"] = wordT
            cypherDict["path similarity"] = pathSimilarityScore
            cypherDict["res similarity"] = resSimilarityScore
            cypherDict["lchScore"] = lchScore
            cypherDict["wupScore"] = wupScore
            cypherDict["jcnSimilar"] = jcnScore
            cypherDict["Lin's measure"] = lin_measurement_score

            ##gsd similarity
            #gsdCypherOut = cyphers.w2wjacard(wordN, wordT)
            #gsdCypherOutDict = gsdCypherOut[0]
            # for key in gsdCypherOutDict:
            #     cypherDict[key] = gsdCypherOutDict[key]

            ##
            cypherRelatedOut = cyphers.word2word(wordN, wordT)
            cypherRelatedOutDict = cypherRelatedOut[0]
            cypherDict["shortestPathSim"] = cypherRelatedOutDict["shortestPathSim"]
            cypherDict["dijkstraPathSim"] = cypherRelatedOutDict["dijkstraPathSim"]

            cypherOut = [cypherDict]
            print(cypherOut)

            # putting all the results above into template
            return render_template("w2w_sim.html", w2word_form=form, cypherOut=cypherOut)
        except Exception as e:
            print("error", e)

    # default results into tamplate
    print(f"default projected graph created: {cyphers.checkExsistsGDSgraph()}")
    cypherOut = [{'sourceNode': 'run', 'targetNode': 'start', 'path similarity': 0.09090909090909091, 'res similarity': 2.036327717785946, 'lchScore': 1.2396908869280152, 'wupScore': 0.4444444444444444, "Lin's measure": 0.2792134381256819}]
    print(cypherOut)
    return render_template("w2w_sim.html", w2word_form=form, cypherOut=cypherOut)

if __name__ == '__main__':
    app.run()
