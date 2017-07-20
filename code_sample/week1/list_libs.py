#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
list installed python packages
"""
import pip
def main():
    tmp = pip.get_installed_distributions()
    installed_libs = sorted(["%s==%s" % (i.key, i.version)
        for i in tmp])
    for s in installed_libs:
        print s

if __name__ == '__main__':
    main()
