#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# change to the location of code (mycodedir) and working direcotry (myworkingdir) (if they are the same, just use same path for both)
mycodedir = '/home/kln/Documents/edu/tmgu17/code_sample/week1'
myworkingdir = '/home/kln/Documents/edu/tmgu17'

import os
os.chdir(mycodedir)
import textminer as tm # importing textminer with alias tm so we only have to write tm. instead of textminer.
os.chdir(myworkingdir)

text = tm.read_txt('DATA/data/pan.txt')
tokens = tm.tokenize(text,1)
tokens_nostop = tm.stopwordfilter(text, 'res/stopword_us.txt')

print text[2000:2100]
print tokens[500:510]
print tokens_nostop[500:510]

from __future__ import division
reduction_ratio = len(tokens_nostop)/float(len(tokens))*100
print 'tokens reduced to', '%.2i' % reduction_ratio, '% of the original number of tokens after stopword removal'

# use quickndirty plots in a similar fashion
os.chdir(mycodedir)
import quickndirty as qd
os.chdir(myworkingdir)

c = 'pan'
x = [int(l == c) for l in tokens]
qd.plotvars(x)
