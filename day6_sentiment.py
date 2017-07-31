#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 11:31:07 2017

@author: kln
"""
import os, re
import textminer as tm
wd = '/home/kln/Documents/edu/tmgu17'
os.chdir(wd)

text = tm.read_txt('DATA/data/pan.txt')

print text[:200]

# use regex to identify START and END of Gutenberg text
pat1 = r'\*{3} START(.*?)\*{3}'
pat2 = r'\*{3} END(.*?)\*{3}'

start_idx = [(m.start(0), m.end(0)) for m in re.finditer(pat1, text)]
end_idx = [(m.start(0), m.end(0)) for m in re.finditer(pat2, text)]

# print start string of Gutenberg text
print text[start_idx[0][0]:start_idx[0][1]]

idx1 = start_idx[0][1]+1 # beginning of content
idx2 = end_idx[0][0]# end of content
# extract text content and assign to variable
content = text[idx1:idx2] 
print content[:100]

tokens = tm.tokenize(content, lentoken = 1)
print tokens[:100]

def slice_tokens(tokens, n = 100, cut_off = True):
    """
    slice tokenized text in slices of n tokens
    - end cut off for full length normalization
    """
    slices = []
    for i in range(0,len(tokens),n):
        slices.append(tokens[i:(i+n)])
    if cut_off:
        del slices[-1]
    return slices

slices = slice_tokens(tokens, 250, True)
print slices[1]

### sentiment analysis with LabMT
import pandas as pd
labmt = pd.read_csv('res/labmt_dict.csv', sep = '\t',
                    encoding = 'utf-8', index_col = 0)

avg = labmt.happiness_average.mean()
sent_dict = (labmt.happiness_average - avg).to_dict()




































