#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
import math, re, string
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
# set working directory
os.chdir(os.path.expanduser('~/Documents/tmgu17/scripts'))
import tmgu as tm
## get data
text_ls, text_names = tm.read_dir_txt('data/')
text = text_ls[3]
tokens = tm.tokenize(text, casefold = True)
## tag could from tokenized text
from wordcloud import WordCloud
# help(WordCloud)# for more information

def tag_cloud(tokens, stop_set = None):
    wc = WordCloud(stopwords = stop_set).generate(' '.join(tokens))
    plt.figure(figsize=(12,12),dpi=200)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    #plt.savefig('wordcloud.png',bbox_inches='tight')
    plt.show()
    plt.close()
# run
tag_cloud(tokens)

### tag cloud based on word counts
def w_count(text):
    """
    raw word counts for full document
    """
    tokens = tm.tokenize(text,casefold = True)
    output = dict([(token, tokens.count(token)) for token in set(tokens)])
    return output
# tag cloud from word frequencies
wf_dict = w_count(text)
wf_sort = sorted(zip(wf_dict.values(), wf_dict.keys()), reverse = True)
wf = [freq for (freq,word) in wf_sort]
lexicon = [word for (freq,word) in wf_sort]

def tag_fr_cloud(wf,lexicon,n = 50):
    dict_n = dict(zip(lexicon[:n],wf[:n]))
    wordcloud = WordCloud(background_color = "white")
    wordcloud.generate_from_frequencies(frequencies=dict_n)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    plt.close()
# run
tag_fr_cloud(wf,lexicon, 10)
