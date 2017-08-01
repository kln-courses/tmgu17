#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
classification of real and fake news using logistic regression
    - data split 80%
    - optimize with IDF weights and bi-grams

"""
import os, re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import metrics
from sklearn.linear_model import LogisticRegressionCV

root = '/home/kln/Documents/edu/tmgu17'
filepath = os.path.join(root,'DATA','fake_or_real_news.dat')
os.chdir(root)
