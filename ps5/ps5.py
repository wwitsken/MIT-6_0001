# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Wesley Witsken
# Collaborators:
# Time:
from abc import ABC

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

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
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        news_story = NewsStory(guid, title, description, link, pubdate)
        ret.append(news_story)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        """
        Initializes a NewsStory object

        guid, title, description, link, pubdate: strings

        NewsStory object has 5 attributes:
            self.guid: globally unique identifier (GUID) - a string
            self.title - a string
            self.description - a string
            self.link to more content - a string
            self.pubdate - a datetime
        """
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        """
        :return: guid (str)
        """
        return self.guid

    def get_title(self):
        """
        :return: title (str)
        """
        return self.title

    def get_description(self):
        """
        :return: description (str)
        """
        return self.description

    def get_link(self):
        """
        :return: link (str)
        """
        return self.link

    def get_pubdate(self):
        """
        :return: pubdate (datetime)
        """
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger, ABC):
    def __init__(self, phrase_trigger):
        """
        :param phrase_trigger: a string
        """
        self.phrase = phrase_trigger.lower()

    def get_phrase(self):
        return self.phrase

    def is_phrase_in(self, text):
        """
        :param text: a string
        :return: (Boolean)
        """
        # Begin by reformatting the text
        # lowercase, replace all punctuation with spaces, strip all those extra spaces
        # remember to leave exactly one space between the words and after the strings, so that they can't be confused
        # if words are smushed together
        spacy_text = " " + text.translate(
            str.maketrans(string.punctuation, ' ' * len(string.punctuation))).lower().strip() + " "
        new_text = re.sub(' +', ' ', spacy_text)
        phrase = " " + self.get_phrase() + " "
        if phrase in new_text:
            return True
        else:
            return False


# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        text = story.get_title()
        return self.is_phrase_in(text)


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        text = story.get_description()
        return self.is_phrase_in(text)


# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, t_time):
        """
        :param t_time: (str) "%d %b %Y %H:%M:%S" (must be EST)
        EG. "3 Oct 2016 17:00:10 "
        """
        self.t_time = datetime.strptime(t_time, '%d %b %Y %H:%M:%S').replace(tzinfo=pytz.timezone("EST"))


# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        pub_date = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        if self.t_time > pub_date:
            return True
        else:
            return False


class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        pub_date = story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))
        if self.t_time < pub_date:
            return True
        else:
            return False


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, T):
        self.T = T

    def evaluate(self, story):
        """
        :param story: NewsStory
        :return: inverted Boolean response of Trigger
        """
        return not self.T.evaluate(story)


# Problem 8
class AndTrigger(Trigger):
    def __init__(self, T1, T2):
        """
        :param T1: Trigger 1
        :param T2: Trigger 2
        """
        self.T1 = T1
        self.T2 = T2

    def evaluate(self, story):
        """
        :param story: NewsStory
        :return: "And" evaluated Boolean of Trigger 1 and Trigger 2
        """
        return self.T1.evaluate(story) and self.T2.evaluate(story)


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, T1, T2):
        """
        :param T1: Trigger 1
        :param T2: Trigger 2
        """
        self.T1 = T1
        self.T2 = T2

    def evaluate(self, story):
        """
        :param story: NewsStory
        :return: "Or" evaluated Boolean of Trigger 1 and Trigger 2
        """
        return self.T1.evaluate(story) or self.T2.evaluate(story)

# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    return stories


# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines)  # for now, print it so you see what it contains!


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
