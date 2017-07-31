#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
EXAMPLE FILE

A collection of my functions for text mining

see: 'how_textminer_module_works.py' for an illustration based on day 4
"""
__author__      = 'Wendy Darling'

# import all modules in beginning of text
import glob, io, os, re

# functions for reading text(s) from a folder
def read_txt(filepath):
    """
    Read txt file from filepath and returns char content in string
    parameters:
        - filepath including filename to file
    """
    with io.open(filepath, 'r', encoding = 'utf-8') as f:
        content = f.read()
    return content

def read_dir_txt(dirpath):
    """
    Import multiple txt file from directory on dirpath
    parameters:
        - path to directory as string

    Return list of strings from txt documents in directory
    """
    filenames = glob.glob(dirpath + '*.txt')
    content_list = []
    for filename in filenames:#loop over filenames
        text = read_txt(filename)# read file
        content_list.append(text)# add file to result list
    return content_list, filenames# return two lists, file content

# functions for tokenizing and cleaning texts
def tokenize(text, lentoken = 0):
    """
    string tokenization and lower-casing for text string
    parameters:
        - text: string to be tokenized
        - lentoken: ignore tokens shorter than or equal to lentoken (default: 0)
    """
    tokenizer = re.compile(r'[^a-zA-Z]+')
    tokens = [token.lower() for token in tokenizer.split(text)
        if len(token) > lentoken]
    return tokens

def stopwordfilter(text, filepath):
    stopword = read_txt(filepath).split()
    tokens_nostop = [token for token in tokenize(text,1) if token not in stopword]
    return tokens_nostop
