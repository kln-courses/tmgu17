#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
- tokenization of single plain text

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
print text# leave metadata

print text[2000:2100]

# list of all tokens in text
import re

def tokenize(text):
    tokenizer = re.compile(r'[^a-zA-Z]*')
    tokens = [token.lower() for token in tokenizer.split(text)]
    return tokens

test = tokenize(text)    
print test[2000:2100]

tokenizer = re.compile(r'[^a-zA-Z]*')
tokens = [token.lower() for token in tokenizer.split(text)]

print tokens[2000:2015]





























