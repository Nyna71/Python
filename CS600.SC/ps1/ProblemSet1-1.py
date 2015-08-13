# -*- coding: utf-8 -*-
"""
Spyder Editor

Paying Off Credit Card Debt.
"""
balance = float(raw_input('Enter the outstanding balance on your credit card: '))
annualInterestRate = float(raw_input('Enter the annual credit card interest rate as a decimal: '))
minimunPaymentRate = float(raw_input('Enter the minimum monthly payment rate as a decimal: '))

print balance, annualInterestRate, minimunPaymentRate

totalAmountPaid = 0.0

for month in range(1, 13):
    print 'Month:', month
    
    minimumMonthlyPayment = round(balance * minimunPaymentRate, 2)
    interestPaid = round(annualInterestRate / 12 * balance, 2)
    principalPaid = round(minimumMonthlyPayment - interestPaid, 2)
    remaingBalance = round(balance - principalPaid, 2)
    
    print 'Minimum monthly payment:', minimumMonthlyPayment
    print 'Principle paid:', principalPaid
    print 'Remaining balance:', remaingBalance
    print '---------------------------------'
    
    balance = remaingBalance
    totalAmountPaid += minimumMonthlyPayment
    
print 'Total Amount Paid:', totalAmountPaid
print 'Remaining Balance:', remaingBalance
    