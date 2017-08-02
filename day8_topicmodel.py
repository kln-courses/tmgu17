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
                paragraph = re.sub(r'[^A-Za-z]',' ',paragraph)
                paragraph = re.sub(r' +',' ',paragraph)
                paragraphs.append(paragraph.rstrip())
    return paragraphs
