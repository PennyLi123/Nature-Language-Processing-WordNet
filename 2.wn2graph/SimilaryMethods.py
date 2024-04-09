# import wordnet & wordnet_ic function
from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic

# load an information content file from the wordnet_ic corpus
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')

##path Similar
def pathSimilar(source, target):
    try:
        # introducing Synsets of source word and target word
        # Take two words' first element in wordnet as input
        word1syn = wordnet.synsets(source)[0]
        word2syn = wordnet.synsets(target)[0]
        pathSimValue = word1syn.path_similarity(word2syn)
        return pathSimValue
    # return a default value when get the corpus incorrectly "e"means exception
    except Exception as e:
        return 0.34

##lch
def lchSimilar(source, target):
    try:
        word1syn = wordnet.synsets(source)[0]
        word2syn = wordnet.synsets(target)[0]
        lch_value=word1syn.lch_similarity(word2syn)
        return lch_value
    except Exception as e:
        return 0.34

##wu pa
def wupSimilar(source, target):
    try:
        word1syn = wordnet.synsets(source)[0]
        word2syn = wordnet.synsets(target)[0]
        wup_value=word1syn.wup_similarity(word2syn)
        return wup_value
    except Exception as e:
        return 0.34

##Lin’s Measure
def linMeasure(source, target):
    try:
        word1syn = wordnet.synsets(source)[0]
        word2syn = wordnet.synsets(target)[0]
        #calculate lin similarity using secmor ic
        lin_measurement_value=word1syn.lin_similarity(word2syn, semcor_ic)
        return lin_measurement_value
    except Exception as e:
        return 0.34



#res Similarity
def resSimilar(source, target):
    try:
        word1syn = wordnet.synsets(source)[0]
        word2syn = wordnet.synsets(target)[0]
        res_sim_value = word1syn.res_similarity(word2syn, brown_ic)
        return res_sim_value
    except Exception as e:
        return 0.34

##Jcn’s Similarity
def jcnSimilar(source, target):
    try:
        word1syn = wordnet.synsets(source)[0]
        word2syn = wordnet.synsets(target)[0]
        jcn_sim_value=word1syn.jcn_similarity(word2syn, brown_ic)
        return jcn_sim_value
    except Exception as e:
        return 0.34


