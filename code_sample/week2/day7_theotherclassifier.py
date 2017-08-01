#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Classification is a supervised learning task, which is one of the central tasks
in machine learning. In this episode we will train several types of supervised
learning algorithms to classify a set of documents according to some classes or
labels (e.g., genre or author features).
"""
__author__= "KLN"

### data preparation ###
from __future__ import division
import io, re, os
import numpy as np
from pandas import DataFrame
from unidecode import unidecode


os.chdir('/home/kln/Documents/tmgu17/scripts')

# include more text normalization
def read_files(path, SPLITCHAR = '\n\n', normalization = False):
    paragraphs_ls, filenames_ls = [], []
    for (root, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root,filename)
            with io.open(filepath, 'r', encoding = 'utf-8') as f:# read text
                text = f.read()
                paragraphs = text.split(SPLITCHAR)# parse paragraphs
                del paragraphs[0]# remove title
                i = 0
                for paragraph in paragraphs:# clean markup
                    paragraph = paragraph.rstrip()
                    if paragraph:
                        if normalization:
                            paragraph = re.sub('\W+',' ', paragraph)
                            paragraph = re.sub('\d','',paragraph)
                            paragraph = unidecode(paragraph.lower())
                        paragraphs_ls.append(paragraph)# append paragraph to list of paragraphs from filepath
                        filenames_ls.append(filename+'_'+str(i))
                        i += 1
    return filenames_ls, paragraphs_ls


def make_df(path, classification):
    filenames, paragraphs = read_files(path, normalization = False)
    rows = []
    idx = []
    i = 0
    for paragraph in paragraphs:
        rows.append({'text': paragraph, 'class': classification})
        idx.append(filenames[i])
        i += 1
    df = DataFrame(rows, index = idx)
    return df

# generate data
NT = 'new_testament'
OT = 'old_testament'

SRCS = [('data_kjv/ot', OT),('data_kjv/nt', NT)]

data = DataFrame({'text': [], 'class': []})
for path, classification in SRCS:
    data = data.append(make_df(path, classification))

data.head()

# unbias data: manage difference in distributions
def printdist(df):
    print 'class distribution:', OT, sum(df['class'] == OT), NT, sum(df['class'] == NT)

printdist(data)

import random
import numpy as np

def unbias_data(df, n):
    random.seed(1234)
    res = DataFrame({'text': [], 'class': []})
    C = list(set(data['class']))
    for c in C:
        idx = df[df['class'] == c].index.tolist()
        df_c = df.loc[random.sample(idx, n),]# label based indexing
        res = res.append(df_c)
    return res.reindex(np.random.permutation(res.index))#shuffle order for classifirer

data_800 = unbias_data(data, 800)
printdist(data_800)

### FEATURE EXTRACTION ###
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()# instantiate vectorizer
raw_fr = vectorizer.fit_transform(data_800['text'].values)

lexicon = vectorizer.vocabulary_
lexicon.keys()
lexicon.values()

### train classifier ###
from sklearn.naive_bayes import MultinomialNB

nb_classifier = MultinomialNB()# instantiate classifier
targets = data_800['class'].values
nb_classifier.fit(raw_fr, targets)

# explore

expl = [data['text'].iloc[-500], data['text'].iloc[10]]# NT/OT
expl = ['Jesus went for a walk on the sea', 'Eve ate the Snake']
expl_raw_fr = vectorizer.transform(expl)
pred = nb_classifier.predict(expl_raw_fr)
print pred

### PIPELINING ###
from sklearn.pipeline import Pipeline
pl = Pipeline([('vectorizer', CountVectorizer()), ('nb_classifier', MultinomialNB())])
pl.fit(data_800['text'].values,data_800['class'].values)

print pl.predict(expl)

### VALIDATION, KFold ###
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score

k_fold = KFold(n = len(data_800), n_folds=5)

scrs = []# performance metrics
confmat = np.array([[0, 0], [0, 0]])
for train_idx, test_idx in k_fold:
    train_feat = data_800.iloc[train_idx]['text'].values
    train_y = data_800.iloc[train_idx]['class'].values

    test_feat = data_800.iloc[test_idx]['text'].values
    test_y = data_800.iloc[test_idx]['class'].values
    # use pipeline
    pl.fit(train_feat, train_y)
    pred = pl.predict(test_feat)

    confmat += confusion_matrix(test_y, pred)
    scr = f1_score(test_y, pred, pos_label = NT)
    scrs.append(scr)


print 'averaged performance:', sum(scrs)/len(scrs)
print confmat# horizontal: predicted label; vertical: true label
print 'accuracy', (confmat[0,0] + confmat[1,1]) / confmat.sum()
# define function for improving classifier
def nb_validation(data, pipe, n_folds = 5):
    k_fold = KFold(n = len(data), n_folds=n_folds)
    scrs = []# performance metrics
    confmat = np.array([[0, 0], [0, 0]])
    for train_idx, test_idx in k_fold:
        train_feat = data.iloc[train_idx]['text'].values
        train_y = data.iloc[train_idx]['class'].values

        test_feat = data.iloc[test_idx]['text'].values
        test_y = data.iloc[test_idx]['class'].values
        # use pipeline
        pipe.fit(train_feat, train_y)
        pred = pl.predict(test_feat)

        confmat += confusion_matrix(test_y, pred)
        scr = f1_score(test_y, pred, pos_label = NT)
        scrs.append(scr)
    print 'averaged performance:', sum(scrs)/len(scrs)
    print confmat# horizontal: predicted label; vertical: true label
    print 'accuracy', (confmat[0,0] + confmat[1,1]) / confmat.sum()




### IMPOROVING RESULTS ###
# include bigrams --> reduce performance
pl = Pipeline([
    ('vectorizer', CountVectorizer(ngram_range=(1, 2))),
    ('nb_classifier',       MultinomialNB())
])

nb_validation(data_800, pl)
# tfidf --> reduce performance
    # notice that MultinomialNB require integer feature counts
        #, but TFIDF fractional counts might also work
from sklearn.feature_extraction.text import TfidfVectorizer

pl = Pipeline([
    ('vectorizer',   TfidfVectorizer()),
    ('nb_classifier',         MultinomialNB())
])

nb_validation(data_800, pl)

## feature selection: univariate feature selection
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2, mutual_info_classif

pl = Pipeline([
('vectorizer', TfidfVectorizer()),
('selector',  SelectKBest(mutual_info_classif, k=1000)),
('nb_classifier', MultinomialNB())
])

nb_validation(data_800, pl)
pl.fit(data_800['text'].values,data_800['class'].values)


# mapping from integer feature name to original token string
feat_names = vectorizer.get_feature_names()
selector =  SelectKBest(mutual_info_classif, k = 100)
raw_fr_k = selector.fit_transform(raw_fr, targets)

feat_names_k = [feat_names[i] for i in selector.get_support(indices = True)]
print feat_names_k

### CLASSIFY DEBATED DOCUMENT ###
lignes = []
with io.open('data_odd/Thomas.txt') as f:
    for line in f.readlines():
        tmp = re.sub(r'Jesus','',line)
        lignes.append(re.sub('\d','',tmp))

pred = pl.predict(lignes)

import matplotlib.pyplot as plt
labels = list(set(pred))
sizes = [sum(pred == label) for label in labels]
explode = (0, .1)
plt.pie(sizes, explode = explode, labels=labels, shadow = True)
plt.axis('equal')
plt.show()
plt.close()

# print OT labelled lines
idx = pred == labels[0]
OT_lignes = [ligne for (ligne, i) in zip(lignes, idx) if i]
for line in OT_lignes:
    print line
