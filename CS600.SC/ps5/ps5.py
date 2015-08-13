# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
        
    def get_guid(self):
        return self.guid
        
    def get_title(self):
        return self.title
        
    def get_subject(self):
        return self.subject
        
    def get_summary(self):
        return self.summary
        
    def get_link(self):
        return self.link
        
    def __str__(self):
        toString = '['
        toString += 'GUID: ' + self.get_guid() + ', '
        toString += 'Title: ' + self.get_title() + ', '
        toString += 'Subject: ' + self.get_subject() + ', '
        toString += 'Summary: ' + self.get_summary() + ', '
        toString += 'Link: ' + self.get_link()
        toString += ']'
        return toString

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger
class WordTrigger(Trigger):        
    def is_word_in(self, text):
        #Ignore punctuation in text to sear
        for c in text:
            if c in string.punctuation:
                text = string.replace(text, c, ' ')
        return self.word.lower() in text.lower().split()
        
    def __init__(self, word):
        self.word = word

class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_title())

class SubjectTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_subject())

class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_summary())

# Composite Triggers
# Problems 6-8

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.otherTrigger = trigger
    
    def evaluate(self, story):
        return not self.otherTrigger.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.t1 = trigger1
        self.t2 = trigger2
        
    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.t1 = trigger1
        self.t2 = trigger2
        
    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t2.evaluate(story)

# Phrase Trigger
# Question 9

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):
        return self.phrase in story.get_title() or \
               self.phrase in story.get_subject() or \
               self.phrase in story.get_summary()
#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """    
    filteredStories = []

    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filteredStories.append(story)

    return filteredStories

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    triggers = {}
    triggerList = []
    
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    for line in lines:
        words = line.split()
        if words[0] == "ADD":
            for trigger in words[1:]:
                triggerList.append(triggers.get(trigger))
        elif words[1] == "TITLE":
            triggers[words[0]] = TitleTrigger(words[2])
        elif words[1] == "SUBJECT":
            triggers[words[0]] = SubjectTrigger(words[2])
        elif words[1] == "PHRASE":
            phrase = ""
            for word in words[2:]:
                phrase += word + " "
            triggers[words[0]] = PhraseTrigger(phrase)
        elif words[1] == "AND":
            triggers[words[0]] = AndTrigger(words[2], words[3])
            
    return triggerList
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    #triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

