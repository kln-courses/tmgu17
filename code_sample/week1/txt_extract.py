#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
converts multiple pdf files to plain text txt files
use: python txt_extract.py /path/to/my/pdffolder
"""

import glob, re, sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

def pdf2txt(path):
    """
    extracts plain text for individual pdf file on path
        - codec: utf-8
        - if embedded password in pdf, password parameter should be updated
    """
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text

def pdf2txt_save(filepath):
    """
    runs and saves output from pdf2txt as ascii
        - modify with io for unicode
    """
    output = pdf2txt(filepath)
    outname = re.sub("\.pdf",".txt",filepath)
    with open(outname,"w") as f:
        f.write(output)

def pdf2txt_multi(dirpath):
    """
    export all files on directory path to pdf2txt_save
    """
    filelist = glob.glob(dirpath + "/*.pdf")
    for filename in filelist:
        print "conversion of "+ filename.split("/")[-1]
        pdf2txt_save(filename)

def main():
    dirpath = sys.argv[1]
    pdf2txt_multi(dirpath)

if __name__ == '__main__':
    main()
