#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
random select, print and save every element from a list 
"""
from numpy.random import choice

def dataimport(fname ='/home/kln/Documents/edu/tmgu17/papers.txt'):
    with open(fname, 'r') as f:
        data = f.read().split(',')
        data = [s.rstrip() for s in data]
    return data

def ordered_list(data):
    o_list = choice(data,len(data), replace = False)
    for i, s in enumerate(o_list):
        print 'Group ' + str(i+1) + ' is', s
    return o_list

def dataexport(data, fname = '/home/kln/Documents/edu/tmgu17/presentation_order.txt'):
    with open(fname, 'w') as f:
        for s in data:
            f.write("%s\n" % s)

def main():
    data = dataimport()
    output = ordered_list(data)
    dataexport(output)

if __name__ == '__main__':
    main()
