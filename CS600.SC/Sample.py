# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 07:33:48 2015

@author: Jonathan Puvilland
"""
x = 12345
epsilon = 0.01
answer = 0.0
nbrGuesses = 0

while abs(answer**2 - x) >= epsilon and answer <= x:
    answer += 0.00001
    nbrGuesses += 1

print 'Nbr of guesses:', nbrGuesses

if abs(answer**2 - x) >= epsilon:
    print 'Failed on square root of', x
else:
    print answer, 'is close of square root of', x
