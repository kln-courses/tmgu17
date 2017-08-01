#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
classification of real and fake news using logistic regression
    - data split 80%
    - optimize with IDF weights and bi-grams

"""

## preamble
from __future__ import division
import os, re
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import metrics
from sklearn.linear_model import LogisticRegressionCV

root = '/home/kln/Documents/edu/tmgu17'
filepath = os.path.join(root,'DATA','fake_or_real_news.dat')
os.chdir(root)

### import and clean data
data = pd.read_csv(filepath)

# inspect classes
print data.label.value_counts()

# clean df by removing non-alphabetic chars
text_clean = []
for text in data['text']:
    text = re.sub(r'[^a-zA-Z]',' ', text)
    text = re.sub(r' +',' ', text)
    text = text.rstrip()
    text_clean.append(text)

# add clean text to df    
data['text_clean'] = text_clean

### set up data set
## split data
ratio = 0.8
mask = np.random.rand(len(data)) < ratio
data_train = data[mask]
data_test = data[~mask]

# control size of data sets
print len(data_train)/len(data)
print len(data_test)/len(data)

### TRAINING (aka representation)

## divide data sets in features X and class y
train_X = data_train['text_clean'].values# features
train_y = data_train['label'].values# classes
# testing/validation
test_X = data_test['text_clean'].values# features
test_y = data_test['label'].values# classes

# minimal pipeline for sklearn training
vecspc = CountVectorizer()# instantiate term frequency vectorizer 
vecspc = TfidfVectorizer()# instantiate TF-IDF vectorizer
vecspc = CountVectorizer(ngram_range=(1,2))# also count bigrams

train_feat = vecspc.fit_transform(train_X)

# inspecting feature names
feat_names = vecspc.get_feature_names()
print len(feat_names)

# train the classifier
clf = LogisticRegressionCV()# instantiate classifier
clf.fit(train_feat, train_y)


## optional: saving your classifier 
import pickle
with open('class_logreg_fake.pcl', 'wb') as file_object:
    pickle.dump(clf, file_object)

# import pickled classifier
clf = pickle.load(open('class_logreg_fake.pcl', 'rb')) 

### VALIDATION 
# test performance
test_feat = vecspc.transform(test_X)
pred = clf.predict(test_feat)

## performance metrics
# confusion matrix
conf_mat = metrics.confusion_matrix(test_y,pred)
print conf_mat
perf_acc = metrics.accuracy_score(test_y, pred)
print perf_acc

# standard performance metric
perf_f1 = metrics.f1_score(test_y, pred, pos_label = 'REAL') 
print perf_f1

print metrics.classification_report(test_y, pred)


### exploring features and document classification
import eli5

# most informative features
eli5.show_weights(clf,vec = vecspc,top =25)

# explore documents
i = 2
text = data['text_clean'][i]
print data.label[i]

obj = eli5.show_prediction(clf,text,vec = vecspc)


























































