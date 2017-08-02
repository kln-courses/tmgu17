#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
TOPIC MODELING
- import paragraphs from text
- preprocess
- merge paragraphs
- train model
- explore model

"""
### preamble
from __future__ import division
import io, os, re
import numpy as np

from nltk.tag import pos_tag
from gensim import corpora, models

root = '/home/kln/Documents/edu/tmgu17'
filepath = os.path.join(root,'DATA','data_rel_full','kjv.txt')
os.chdir(root)

import textminer as tm

def get_para(filepath, encoding = 'utf-8'):
    """
    Import text file on filepath in paragraphs
    - default encoding unicode
    """
    with io.open(filepath, "r", encoding = encoding) as f:
        text = f.read()
        paragraphs = []
        for s in text.split('\n\n'):
            if s:
                paragraph = s#.lower()
                #paragraph = re.sub(r'\W',' ',paragraph)
                #paragraph = re.sub(r'\d',' ',paragraph)
                paragraph = re.sub(r'[^A-Za-z]',' ',paragraph)
                paragraph = re.sub(r' +',' ',paragraph)
                paragraphs.append(paragraph.rstrip())
    return paragraphs

paragraphs = get_para(filepath)
print paragraphs[0]

### parts of speech tagging
print pos_tag(tm.tokenize(paragraphs[100]), tagset = 'universal', lang = 'eng')

# monster tokenizer that includes specific part of speech
i = 0
para_token = []
for paragraph in paragraphs:
    print i
    tokens = tm.tokenize(paragraph, length = 1, casefold = False)
    tagset = pos_tag(tokens, tagset = 'universal', lang = 'eng')
    tokens = [tag[0] for tag in tagset if tag[1] in ['NOUN']]
    tokens = [token.lower() for token in tokens]
    para_token.append(tokens)
    i += 1

print para_token[100]
# generate stopword list from text
sw = tm.gen_ls_stoplist(para_token,10)


# merge paragraphs in list of n paragraphs to get longer documents
data_premerge = para_token
data = []
n = 10
idx = range(0,len(data_premerge),n)
for i in idx:
    if i == max(idx):
        merge = data_premerge[i]
        for ii in range(i+1, len(data_premerge)):
            merge = merge + data_premerge[ii]
    else:
        merge = data_premerge[i]
        for ii in range(1,n):
            merge = merge + data_premerge[i+ii]
    data.append(merge)
        
print len(data)
print len(data_premerge)
### let the topic modeling begin
dictionary = corpora.Dictionary(data)

print dictionary.num_docs
print dictionary.items()
print dictionary.keys()
print dictionary.values()
print dictionary.dfs

# bag-of-words representation of the paragraphs
text_bow = [dictionary.doc2bow(text) for text in data]

paragraph_bow = [dictionary.doc2bow(paragraph) for paragraph in data]
i = -1500
print data[i]
paragraph = paragraph_bow[i]
print paragraph

# train the model
k = 10
mdl = models.LdaModel(text_bow, id2word = dictionary, 
                      num_topics = k, random_state = 1234)

## explore the model
# print topics as word distributions 
for i in range(k):
    print 'Topic',i
    print [t[0] for t in mdl.show_topic(i,10)]
    print '-----'
    

print paragraph
print mdl[paragraph]
print data

# query the document with unseen documents
query = u'Jesus was a jew who loved Israel people'
query = query.lower().split()
vocab = dictionary.values()
query = [w for w in query if w in vocab]
print query
query = dictionary.doc2bow(query)
print query
mdl[query]
print mdl.show_topic(7,10)

## estimate document similarity on topic
# KL divergence
def get_theta(doc_bow, mdl):
    tmp = mdl.get_document_topics(doc_bow, minimum_probability=0)
    return [p[1] for p in tmp]

def kl_div(p, q):
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
    return np.sum(np.where(p != 0,(p-q) * np.log10(p / q), 0))

para1 = paragraph_bow[1]
para2 = paragraph_bow[-100]
para3 = paragraph_bow[2]

print kl_div(get_theta(para1, mdl), get_theta(para2, mdl))
print kl_div(get_theta(para1, mdl), get_theta(para3, mdl))



