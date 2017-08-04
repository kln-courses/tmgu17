#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Because word meaning depends critically on their context, this episode will
introduce several techniques to model word context and word associations.
We will look at ngram, KWIC search, co-occurrence matrix, measures of word collocations,
and similarity-based measures for vector spaces.

develop simple KWIC algorithm based on ngrams
"""
__author__= "KLN"

from __future__ import division
import math, re
import tmgu as tm
import matplotlib.pyplot as plt
## get data
#text = tm.getpan()
text = tm.read_txt('/home/kln/Documents/tmgu17/scripts/data/pan.txt')
tokens = tm.tokenize(text, length = 1, casefold = True)# remove single character endings in e.g., can't

def ngram_get(tokens, n = 2):
    """
    token list of length n of tokenized document with (max overlap)
    """
    return [tokens[i:i+n] for i in range(len(tokens)-(n-1))]

ngram_tokens = ngram_get(tokens, 3)
print ngram_tokens[49]

from collections import defaultdict
def ngram_count(tokens, n = 2):
    """
    ngram frequencies of tokenized documents (max overlap)
    """
    ngram_tokens = ngram_get(tokens, n)
    res = defaultdict(int)
    ngrams = [" ".join(ngram) for ngram in ngram_tokens]
    for ngram in ngrams:
        res[ngram] += 1
    return res

ngram_fr = ngram_count(tokens, 3)
type(ngram_fr)
ngram_sort = sorted(zip(ngram_fr.values(),ngram_fr.keys()), reverse = True)

## let's go Zipf on ngrams
y = [i[0] for i in ngram_sort]
def letszipf(y):
    """
    loglog plot of y term frequencies
    """
    ylog = [math.log(yi) for yi in y]
    xlog = [math.log(xi) for xi in range(1,len(y)+1)]
    tm.qd_plot(xlog,ylog)

letszipf(y)
# let's go Zipf on proportions

def qd_bar(y, sv = False, filename = 'qd_bar.png', ax1 = '$x$', ax2 = '$f(x)$'):
    """
    quick and dirty bar plot of one variable
    """
    fig, ax = plt.subplots()
    x = range(1,len(y)+1)
    ax.bar(x,y,color = 'k')
    ax.set_xlabel(ax1)
    ax.set_ylabel(ax2)
    if sv:
        plt.savefig(filename, dpi = 300)
    else:
        plt.show()
        plt.close()

def letszipf_plus(y, n = 10):
    """
    test of zipf: he frequency of any word is inversely proportional to its rank in the frequency table
    bar plot of n max word frequencies divided by max word frequency
    """
    prop = [y[0]/yi for yi in y[:n]]
    qd_bar(prop,ax1 = 'Rank', ax2 = 'Proportion')

letszipf_plus(y)

## keyword in context

ngram_tokens = ngram_get(tokens, 5)# use +/-2 context, get middle by floor division

def get_kwic(ngram_tokens):
    """
    returns dictionary of keywords in context
    """
    kw_i = len(ngram_tokens[0]) // 2# floor division, get location of keyword/middle of each ngram_token
    kwic_dict = {}
    for ngram in ngram_tokens:
        if ngram[kw_i] not in kwic_dict:
            kwic_dict[ngram[kw_i]] = [ngram]
        else:
            kwic_dict[ngram[kw_i]].append(ngram)
    return kwic_dict

kwic = get_kwic(ngram_tokens)
kwic['tinker']
