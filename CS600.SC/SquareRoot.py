# -*- coding: utf-8 -*-
"""
SquareRoot.py
Calculates an approximation of the square root for a given number (x) and an
error margin (epsilon)

Created on Mon Jun 22 07:33:48 2015

@author: Jonathan Puvilland
"""
x = float(raw_input('Enter a number for which you want to calculate the Square root: '))
epsilon = float(raw_input('Enter an error margin (ex. 0.001): '))
nbrGuesses = 0
low = 0.0
high = x
answer = (low + high) / 2.0

while abs(answer**2 - x) >= epsilon and answer <= x:
    nbrGuesses += 1
    # Current estimation is too high
    if answer**2 < x:
        low = answer
    else:
        high = answer
    answer = (low + high) / 2.0

print 'Nbr of guesses:', nbrGuesses

if abs(answer**2 - x) >= epsilon:
    print 'Failed on square root of', x
else:
    print answer, 'is close of square root of', x
    print answer, '**2 = ', answer**2 
