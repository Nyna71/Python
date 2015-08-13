# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "../words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    #return random.choice(wordlist)
    return 'Novak Djokovic'

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()
wordToGuess = choose_word(wordlist)

def print_game_status(nbrGuessLeft, availableLetters, wordInGuess):
    print '-----------------------------------------------------------'
    print 'You have', nbrGuessLeft, 'guesses left.'
    print 'Current guess: ', wordInGuess
    print 'Available letters: ', availableLetters

def init_game():
    print 'Welcome to the game, Hangman!'
    print 'I am thinking of a word that is', len(wordToGuess) , 'letters long.'
    
    wordInGuess = ''
    for i in range(0, len(wordToGuess) + 1):
         wordInGuess += '-'
        
    return wordInGuess

def letterFound(letter, wordToGuess, wordInGuess):
    """ Returns a new wordInGuess String where each occurences of the guessed
        letter replaces the corresponding dashes in the wordInGuess String
    """
    returnWord = '' 
    
    for i in range(0, len(wordToGuess)):
        if(wordToGuess[i] == letter):
            returnWord += wordToGuess[i]
        else:
            returnWord += wordInGuess[i]
    
    return returnWord

# your code begins here!
def runGame():
    nbrGuessLeft = 8
    availableLetters = list('abcdefghijklmnopqrstuvwxyz')
    wordInGuess = init_game()
    
    while(True):
        print_game_status(nbrGuessLeft, availableLetters, wordInGuess)
        letter = raw_input('Please guess a letter: ')
        
        letterIndex = string.find(wordToGuess, letter)
        if(availableLetters.__contains__(letter)):
            availableLetters.remove(letter)
        else:
            print 'You already choose the letter:', letter
        
        if(letterIndex == -1):
            print 'Oops! That letter is not in my word'
            nbrGuessLeft -= 1
            if(nbrGuessLeft == 0):
                print 'Lost, word to guess was: ', wordToGuess
                break
        else:
            wordInGuess = letterFound(letter, wordToGuess, wordInGuess)
            if(string.find(wordInGuess, '-') == -1): #All letters have been found
                print 'Great, you found the word: ', wordInGuess
                break

runGame()