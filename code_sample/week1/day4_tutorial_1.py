#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
- tokenization of single plain text
- count word frequencies
- plot word frequencies
"""
# preamble: setting up my python session
import os, io, glob
wd = '/home/kln/Documents/edu/tmgu17'# absolute path to session working directory
os.chdir(wd)
data_path = 'DATA/data/'# relative path to data

def read_txt(filepath):
    """
    Read txt file from filepath and returns char content
    in string
    """
    with io.open(filepath, 'r', encoding = 'utf-8') as f:
        content = f.read()
    return content

def read_dir_txt(dirpath):
    """
    Import multiple txt file from directory on dirpath
    - Return as list of strings
    """
    filenames = glob.glob(dirpath + '*.txt')
    result_list = []
    for filename in filenames:#loop over filenames
        text = read_txt(filename)# read file
        result_list.append(text)# add file to result list
    return result_list, filenames# return two lists, file content

# single text tokenization
text = read_txt('DATA/data/pan.txt')

# list of all tokens in text
import re

def tokenize(text, lentoken = 0):
    """
    string tokenization for characters only
    - case-fold: lower
    -
    """
    tokenizer = re.compile(r'[^a-zA-Z]+')
    tokens = [token.lower() for token in tokenizer.split(text)
        if len(token) > lentoken]
    return tokens

tokens = tokenize(text,1)# tokenize and remove single character tokens (1)

## stopword filtering
# import stopwords (very restrictive list)
stopword = read_txt('res/stopword_us.txt').split()
# tokenize and ignore tokens (i.e., words) in stopword list
tokens_nostop = [token for token in tokenize(text,1) if token not in stopword]

# token reduction
from __future__ import division
reduction_ratio = len(tokens_nostop)/float(len(tokens))*100
print 'tokens reduced to', '%.2i' % reduction_ratio, '% of the original number of tokens after stopword removal'

### WORD COUNTING
def tf(term, tokens):
    """
    Raw term frequency
    """
    result = tokens.count(term)
    return result

print tf('pan',tokens_nostop)

# lexicon of unique words (types) in text
lexicon = set(tokens_nostop)
# count all tokens (words) of all types in lexicon
tf_all = dict([(token, tokens_nostop.count(token)) for token in lexicon])

# word search in Peter Pan (or any other text that I import)
print tf_all['pan']
print tf_all['wendy']
hate_love_ratio = tf_all['love']/tf_all['hate']
print 'the ratio of love to hate is %.2i' % hate_love_ratio

### plotting of word distribution in the text
import matplotlib as mpl
import matplotlib.pyplot as plt

def plotvars(x , sv = False, filename = 'qd_plot.png'):
    """
    quick and dirty x axis plotting
    parameters:
        - x: list of numerical values
        - sv: save (default: False)
        - filename: filename of saved plot (default: qd_plot.png)
    """
    fig, ax = plt.subplots()
    ax.plot(x, color = 'k', linewidth = .1)
    ax.set_xlabel('Time')
    ax.set_ylabel('Y')
    if sv:
        plt.savefig(filename, dpi = 300)
    else:
        plt.show()
    plt.close()

# plot dispersion of 'pan'
c = 'wendy'
x = [int(l == c) for l in tokens]
plotvars(x)

# plot dispersion of peter + pan
import numpy as np
c1 = 'peter'
c2 = 'pan'
x1 = [int(l == c1) for l in tokens]
x2 = [int(l == c2) for l in tokens]
x1x2 = [sum(x) for x in zip(x1, x2)]
plotvars(x1x2)

# plot dispersion of multiple keywords
import matplotlib.pyplot as plt
def disp_plot(text,kws):
    """
    dispersion plot for multiple keywords
    parameters:
        - text: input string
        - kws: list of keywords
    """
    kws = [kw.lower() for kw in kws]
    tokens = tokenize(text)
    pts = [(x,y) for x in range(len(tokens)) for y in range(len(kws)) if tokens[x] == kws[y]]
    if pts:
        x,y = zip(*pts)
    else:
        x = y = ()
    plt.plot(x,y,"k.")
    plt.yticks(range(len(kws)),kws,color="k")
    plt.ylim(-1,len(kws))
    plt.title("Lexical Dispersion Plot")
    plt.xlabel("Word Offset")
    plt.show()

ws = ['peter','pan']
disp_plot(text,ws)
