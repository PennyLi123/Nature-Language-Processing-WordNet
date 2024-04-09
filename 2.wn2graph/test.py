# -*- coding: utf-8 -*-
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic


dog = wn.synset('dog.n.01')
cat = wn.synset('cat.n.01')

brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')

dog.path_similarity(cat)

dog.jcn_similarity(cat, brown_ic)
dog.lin_similarity(cat, semcor_ic)

dog.res_similarity(cat, brown_ic)