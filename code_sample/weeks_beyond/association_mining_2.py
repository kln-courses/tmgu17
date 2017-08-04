#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Because word meaning depends critically on their context, this episode will
introduce several techniques to model word context and word associations.
We will look at ngram, KWIC search, co-occurrence matrix, measures of word collocations,
and similarity-based measures for vector spaces.
"""
__author__= "KLN"

from __future__ import division
import math, re, string
import tmgu as tm
## get data
#text = tm.getpan()
text = tm.read_txt('/home/kln/Documents/tmgu17/scripts/data/pan.txt')
tokens = tm.tokenize(text, length = 1, casefold = True)

## co-occurrence
from collections import defaultdict
def cooccur_matrix(multi_tokens):
    mat = defaultdict(lambda : defaultdict(int))
    for tokens in multi_tokens:
        for i in xrange(len(tokens)-1):
            for j in xrange(i+1, len(tokens)):
                t1, t2 = [tokens[i], tokens[j]]
                mat[t1][t2] += 1
                mat[t2][t1] += 1
    return mat

test = [['he','likes','apples'],['she','hates','apples'],['he','likes','juniper']]
cc_mat = cooccur_matrix(test)
cc_mat.items()
cc_mat['likes'].items()
# co-occurrence for sentences
import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sents = tokenizer.tokenize(text)
sents_tokens = [tm.tokenize(sent, 0, True) for sent in sents]
cc_mat = cooccur_matrix(sents_tokens)

## calculate PMI (association measure)
w1 = 'peter'
w2 = 'pan'
ngram_n = len(sents)# total number of ngrams
p_w1w2 = cc_mat[w1][w2]/ngram_n# joint probability
# individual probabilities
freqs = tm.w_count(text)# word frequencies
w_n = sum(freqs.values())# total number of words
p_w1 = freqs[w1]/w_n# w1 probability
p_w2 = freqs[w2]/w_n# w2 probability
pmi = math.log(p_w1w2/(p_w1*p_w2))
print pmi

### collocation
# nltk
import nltk
from nltk.collocations import *
atext = nltk.Text(tokens)
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words((atext))
finder.apply_freq_filter(5)

bigram_measures.student_t

print finder.nbest(bigram_measures.pmi, 20)
print finder.nbest(bigram_measures.likelihood_ratio, 20)
for i in finder.score_ngrams(bigram_measures.pmi):
    print i

trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = TrigramCollocationFinder.from_words((atext))
finder.apply_freq_filter(5)
for i in finder.score_ngrams(trigram_measures.pmi):
    print i

## document similarity: Jaccard Similarity
def jaccard_sim(query, document):
    """
    jaccard similarity for query to document
    * notice bow assumption
    """
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)

# compare text re-use at sentence level
q = sents_tokens[1100]
jac_list = []
for sent in sents_tokens:
    jac_list.append(jaccard_sim(q,sent))
tm.plotdist(jac_list)
print jac_list.index(max(jac_list))
minidx = [i for i, value in enumerate(jac_list) if value == min(jac_list)]
print str(len(minidx))+' sentences are orthogonal to: ' + " ".join(q)

## document similarity: cosine similarity
# similarity measure for vector space representations
import textmining
dtm = textmining.TermDocumentMatrix()
for sent in sents:
    dtm.add_doc(sent)
dtm_list = []
for row in dtm.rows():
    dtm_list.append(row)

lexicon = dtm_list[0]
del dtm_list[0]

v1 = dtm_list[1100]
idx = [i for i, value in enumerate(v1) if value > 0]# find indices for terms in v1
for i in idx:# print words in v1
    print lexicon[i]

v2 = dtm_list[5]#orthogonal document

def cosine_similarity(vector1, vector2):
    """
    cosine similarity between two document vectors
    * notice bow assumption
    """
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude

print cosine_similarity(v1, v1)
print cosine_similarity(v1, v2)

## deep learning like word associations
