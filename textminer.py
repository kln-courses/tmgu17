#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
EXAMPLE FILE

A collection of my functions for text mining

see: 'how_textminer_module_works.py' for an illustration based on day 4
"""
__author__      = 'Wendy Darling'

# import all modules in beginning of text
import glob, io, math, os, re,  string
from collections import defaultdict
from operator import itemgetter
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

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
def tokenize(input, length = 0, casefold = False):
    """
    string tokenization and lower-casing for text string
    parameters:
        - text: string to be tokenized
        - lentoken: ignore tokens shorter than or equal to lentoken (default: 0)
    """
    if type(input) == unicode:
        #tokenizer = re.compile('\W+', re.UNICODE)
        tokenizer = re.compile(r'[^A-Za-z]+', re.UNICODE)
    else:
        tokenizer = re.compile(r'[^A-Za-z]+')
    if casefold:
        input = input.lower()
    tokens = [token for token in tokenizer.split(input) if len(token) > length]
    return tokens

def stopwordfilter(text, filepath):
    stopword = read_txt(filepath).split()
    tokens_nostop = [token for token in tokenize(text,1) if token not in stopword]
    return tokens_nostop

def gen_ls_stoplist(input, n = 100):
    """
    generate stopword list from list of tokenized text strings
    """
    t_f_total = defaultdict(int)
    #n = 100
    for text in input:
        for token in text:
            t_f_total[token] += 1
    nmax = sorted( t_f_total.iteritems(), key = itemgetter(1), reverse = True)[:n]
    return [elem[0] for elem in nmax]

def prune_multi(input, t_r_min = 1, n_max = 0):
    """
    prune bottom and top of list of tokenized strings
    - t_r_min: minimum term frequency
    - n_max: n most frequent words to remove
    """
    t_f_total = defaultdict(int)
    for text in input:
        for token in text:
            t_f_total[token] += 1
    nmax = sorted( t_f_total.iteritems(), key = itemgetter(1), reverse = True)[:n_max]
    stoplist = [elem[0] for elem in nmax]
    output_ls = []
    for text in input:
        output = [token for token in text if t_f_total[token] >= t_r_min and token not in stoplist]
        output_ls.append(output)
    return output_ls

def treebank2wordnet(treebank_tag):
    """
    map treebank pos tags to wordnets four categories:
    - n: noun (default), v: verb, a: adjective, and r: adverbs
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def pos_sensitive_lemmatizer(tokens):
    """
    lemmatizer with treebank pos tags
    """
    tokens_tag = pos_tag(tokens, tagset = 'universal', lang = 'eng')
    lemmatizer = WordNetLemmatizer()
    output = []
    for i in range(len(tokens_tag)):
        output.append(lemmatizer.lemmatize(tokens_tag[i][0],
        treebank2wordnet(tokens_tag[i][1])))
    return output
