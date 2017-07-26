#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
- how to import and export plain text


"""

# preamble: setting up my python session
import os, io, glob
wd = '/home/kln/Documents/edu/tmgu17'# absolute path to session working directory
os.chdir(wd)
data_path = 'data/'# relative path to data
filenames = os.listdir(data_path)

# illustrate that filenames is a list of strings
print filenames
for s in filenames:
    print s.upper()
print type(filenames[0])

filename = data_path + filenames[2]
filename = 'data/pan.txt'

### import on text that might have unicode characters
## two similar modes of importing
# mode 1
f = io.open(filename, 'r', encoding = 'utf-8')
content = f.read()
f.close()
# mode 2
with io.open(filename, 'r', encoding = 'utf-8') as f:
    content = f.read()

#object type?
print type(content)
# length?
print len(content)
# first 1000 characters
print content[0:1000]
# case-fold content
lowpan = content.lower()
print lowpan[:1000]


def read_txt(filepath):
    """
    Read txt file from filepath and returns char content
    in string
    """
    f = io.open(filepath, 'r', encoding = 'utf-8')
    content = f.read()
    f.close()
    return content


filename = data_path + filenames[0]

text = read_txt(filename)
print text[:1000]

## import multiple files from directory
lit_list = []
for filename in filenames:
    filepath = data_path + filename
    text = read_txt(filepath)
    lit_list.append(text)

print 'start 10 chars in', filenames[0], ':'
print lit_list[0][:1000]

# lower case all files from directory and store in list
lit_list = []
for filename in filenames:
    filepath = data_path + filename
    text = read_txt(filepath)
    textlow = text.lower()
    lit_list.append(textlow)

### my functions for reading plain text files
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
    return result_list, filenames# return two lists, file content and file name    

someones_corpus, someones_filenames = read_dir_txt(data_path)




