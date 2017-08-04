#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Word embedding algorithms have become popular tools for uncovering the full
associative structure of large text collections. Using an artificial neural
network, we can construct high-dimensional vector representations of words,
sentences, and documents and explore their similarity structure.
"""
__author__="KLN"

import io, re, math

filepath = '/home/kln/Documents/tmgu17/scripts/data_rel_full/kjv.txt'

# lignes
tokenizer = re.compile(r'[^A-Za-z]+')
data = []
with io.open(filepath, 'r', encoding = 'utf-8') as f:
    lignes = [tokenizer.split(line.rstrip()) for line in f.readlines() if line.rstrip()]
    for tokens in lignes:
        tokens = [token.lower() for token in tokens if token]
        data.append(tokens)

# sentences
import nltk.data
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
tokenizer = re.compile(r'[^a-zA-Z]+')
data = []
with io.open(filepath, 'r', encoding = 'utf-8') as f:
    text = f.read()
    for sent in sent_tokenizer.tokenize(text):
        tokens = tokenizer.split(sent)
        tokens = [token.lower() for token in tokens if token]
        data.append(tokens)


from gensim import models
mdl = models.Word2Vec(data, size = 100, window = 5, seed = 1234, min_count = 5, workers = 2)
# size is the dimensionality of the feature vectors.
# window is the maximum distance between the current and predicted word within a sentence
# alpha is the initial learning rate (will linearly drop to min_alpha as training progressesmin_count = ignore all words with total frequency lower than this.#
# workers = use this many worker threads to train the model (=faster training with multicore machines).

# distributed representation
print mdl.wv['god']


## you can perform various NLP word tasks with the model. Some of them are already built-in:
# Find the top-N most similar words. Positive words contribute positively towards the similarity, negative words negatively.
similar_words_list = mdl.wv.most_similar(positive=['god'])
mdl.wv.most_similar(positive=['god'],negative = ['jesus'])

print "God's similarity to:"
print
print 'Jesus: ', mdl.wv.similarity('god', 'jesus')
print 'Man: ', mdl.wv.similarity('god', 'man')
print 'Woman: ', mdl.wv.similarity('god', 'woman')

# complex comparisons
mdl.wv.most_similar(positive=['jesus', 'god'], negative = ['lord'])
mdl.wv.most_similar(positive=['woman', 'king'], negative = ['man'])# classic exammple
# Find the top-N most similar words, using the multiplicative combination objective proposed by Omer Levy and Yoav Goldberg
mdl.wv.most_similar_cosmul(positive=['woman', 'king'], negative=['man'])

# does not match set
mdl.wv.doesnt_match("jesus god woman man wine".split())

### a bug report submitted
## Probability of a text under a vector space model:
# need to train with hierarchical softmax
mdl2 = models.Word2Vec(data, size = 100, window = 5, seed = 1234,
min_count = 1, workers = 2, hs = 1, negative = 0)
text1 = "god walked on the wine".split()
text2 = "mr. hansen drank the wine".split()
log_props = mdl2.score(text1)
props = [math.exp(log_prop) for log_prop in log_props]
print props

# a picture of god
import matplotlib.pyplot as plt
plt.matshow(mdl['god'].reshape((10,10)), fignum = 100, cmap=plt.cm.gray)
plt.show()

mdl.finalize_vocab

####
