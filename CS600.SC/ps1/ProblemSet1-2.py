# -*- coding: utf-8 -*-
"""
Spyder Editor

Paying Off Credit Card Debt.
"""

def getRemainingBalance(monthlyPayment, balance, monthlyInterestRate):
    """
    This function calculates the remaining balance after applying one year of monthly payments
    on which a monthly interest rate is also applied.
    """
    numberOfMOnthNeeded = 0
    for i in range (0, 12):
        numberOfMOnthNeeded += 1
        balance = round(balance * (1 + monthlyInterestRate) - monthlyPayment, 2)
        if balance < 0:
            print 'Number of month needed:', numberOfMOnthNeeded
            break
    return balance

balance = float(raw_input('Enter the outstanding balance on your credit card: '))
annualInterestRate = float(raw_input('Enter the annual credit card interest rate as a decimal: '))
print

totalAmountPaid = 0.0
monthlyInterestRate = annualInterestRate / 12.0
paymentIncrement = 0.01

# Applying Bisection search to reduce the number of valid monthly payment cases to look for
monthlyPaymentLowerBound = balance / 12.0
monthlyPaymentUpperBound = (balance * (1 + (annualInterestRate / 12.0)) ** 12.0) / 12.0

monthlyPayment = monthlyPaymentLowerBound

while (monthlyPayment <= monthlyPaymentUpperBound):
    remainingBalance = getRemainingBalance(monthlyPayment, balance, monthlyInterestRate)
    if remainingBalance < 0:
        print 'Remaining balance after 1 year of', round(monthlyPayment, 2), 'monthly payments:', round(remainingBalance, 2)
        break
    monthlyPayment += paymentIncrement