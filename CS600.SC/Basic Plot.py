# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 16:57:48 2015

@author: Jonathan
"""

import pylab
import random
import math

def stdDev(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return math.sqrt(tot/len(X))

def flip(numFlips):
    heads = 0
    for i in range(numFlips):
        if random.random() < 0.5:
            heads += 1
    return heads / float(numFlips)

def flipSim(numTrials, numFlips):
    fracHeads = []
    for i in range(numTrials):
        fracHeads.append(flip(numFlips))
    print "Results:", fracHeads
    print "Mean:", sum(fracHeads) / len(fracHeads)
    print "Standard Deviation", stdDev(fracHeads)


