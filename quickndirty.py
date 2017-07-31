#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def plotdist(x, sv = 0, filename = "dist.png"):
    """ histogram with normal fit """
    mu = np.mean(x)
    sigma =  np.std(x)
    n, bins, patches = plt.hist(x, 50, normed=1, facecolor='k', alpha=0.75)
    y = mlab.normpdf(bins, mu, sigma)# best normal fit
    ax = plt.plot(bins, y, 'r--', linewidth=1)
    plt.ylabel('Probability')
    plt.grid(True)
    if sv == 1:
        plt.savefig(filename, dpi = 300)
    else:
        plt.show()
        plt.close()

def plotvars(x,y = 0, sv = False, filename = 'qd_plot.png', ax1 = 'x', ax2 = 'f(x)'):
    """
    quick and dirty x and x-y plotting
    """
    fig, ax = plt.subplots()
    if y:
        ax.plot(x,y, color = 'k')
        ax.set_xlabel(ax1)
        ax.set_ylabel(ax2)
    else:
        ax.plot(x, color = 'k', linewidth = .3)
        ax.set_xlabel(ax1)
        ax.set_ylabel(ax2)
    if sv:
        plt.savefig(filename, dpi = 300)
    else:
        plt.show()
        plt.close()

def plotbar(y, sv = False, filename = 'qd_bar.png', ax1 = 'x', ax2 = 'f(x)'):
    """
    quick and dirty bar plot of one variable
    """
    fig, ax = plt.subplots()
    x = range(1,len(y)+1)
    ax.bar(x,y,color = 'k')
    ax.set_xlabel(ax1)
    ax.set_ylabel(ax2)
    if sv:
        plt.savefig(filename, dpi = 300)
    else:
        plt.show()
        plt.close()
