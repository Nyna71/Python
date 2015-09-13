# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

import string

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename=SHORT_SUBJECT_FILENAME):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    subjects = {}
    
    inputFile = open(filename)
    for line in inputFile:
        if len(line) == 0 or line[0] == '#':
            continue
        dataLine = string.split(line, sep=",")
        courseName = dataLine[0]
        valueworkTuple = (string.atoi(dataLine[1]), string.atoi(dataLine[2]))
        
        subjects[courseName] = valueworkTuple
        #print "Course Name:", courseName, "valueworkTuple:", valueworkTuple
    
    return subjects

    # TODO: Instead of printing each line, modify the above to parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    if subInfo1[VALUE] == subInfo2[VALUE]:
        return subInfo1[WORK] < subInfo2[WORK]
    else:
        return subInfo1[VALUE] > subInfo2[VALUE]

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    if subInfo1[WORK] == subInfo2[WORK]:
        return subInfo1[VALUE] > subInfo2[VALUE]
    else:
        return subInfo1[WORK] < subInfo2[WORK]

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    return float(subInfo1[VALUE])/subInfo1[WORK] > float(subInfo2[VALUE])/subInfo2[WORK]

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    currentWork = 0
    bestSubjects = {}
    remainingSubjects = subjects.copy()
    
    while currentWork < maxWork and len(remainingSubjects) > 0:
        subject, valueworkTuple = findBestSubject(remainingSubjects, comparator)
        
        #Check if next best subject do not overload the maximum work allowed
        if valueworkTuple[WORK] <= (maxWork - currentWork):
            bestSubjects[subject] = valueworkTuple
            currentWork += valueworkTuple[WORK]
        
        remainingSubjects.pop(subject) 
    
    return bestSubjects

def findBestSubject(subjects, comparator):
    """
    Returns a course subject name and a (value, work) tuple amongst a list of subject,
    which maximizes the comparator function (ex. subject with highest value or lowest work).

    subjects: dictionary mapping subject name to (value, work)
    comparator: function taking two tuples and returning a bool
    returns: a subject name and (value, work) tuple
    """
    bestKey, bestValue = subjects.popitem()
    subjects[bestKey] = bestValue
    
    for key in subjects.iterkeys():
        if comparator(subjects.get(key), bestValue):
            bestKey = key
            bestValue = subjects.get(key)
            
    return bestKey, bestValue
    
#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm. bruteForce is a recursive algorithm calling itself with a
    reduce list of subjects at every call.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """    
    if len(subjects) == 0:
        return {}
    
    remainingSubjects = subjects.copy()
    
    #First case: we include a subject the current list if it does not overload the
    #maximum work
    key, valueworkTuple = remainingSubjects.popitem()
    case1 = {}
    if valueworkTuple[WORK] <= maxWork:
        case1[key] = valueworkTuple
        case1.update(bruteForceAdvisor(remainingSubjects, maxWork - valueworkTuple[WORK]))

    #Second case: we do not include the key in the current list
    case2 = bruteForceAdvisor(remainingSubjects, maxWork)
    
    #Evaluate which case gives the best value and returns it
    if evaluateSubjects(case1) > evaluateSubjects(case2):
        return case1
    else:
        return case2

def evaluateSubjects(subjects):
    totalValue = 0
    for key in subjects.iterkeys():
        valueworkTuple = subjects.get(key)
        totalValue += valueworkTuple[VALUE]
        
    return totalValue
