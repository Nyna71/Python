#from ps3a import *
import ps3a as ps3a
import time
from perm import *

#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    # TO DO...
    maxScore = 0
    maxWord = ''
    n = calculate_handlen(hand)
    
    while(n > 0):
        permList = get_perms(hand, n)

        for word in permList:
            #print word
            if(is_valid_word(word, hand, word_list)):
                #print 'Valid word:', word
                score = get_word_score(word, HAND_SIZE)
                if(score > maxScore):
                    #print 'Max Score', score, 'for word', word
                    maxWord = word
                    maxScore = score
        n -= 1
    
    return maxWord
#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # TO DO ...    
    totalScore = 0    
    
    while(True):
        print 'Current hand:'
        display_hand(hand)
        print 'Computer chooses a word...'
        word = comp_choose_word(hand, word_list)

        if(word != ''):
            score = get_word_score(word, HAND_SIZE)
            totalScore += score
            print '"'+ word, '" earned', score, 'points. Total:', totalScore, 'points.'
            hand = update_hand(hand, word)
            if(calculate_handlen(hand) == 0):
                break
        else:
            print 'No more valide words.'
            break
            
    print 'Computer Total score:', totalScore, 'points'
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...
    ps3a.play_game(word_list)
    comp_play_hand(hand, word_list)
    
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    
