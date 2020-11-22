import urllib.request
import urllib.error
import re
from textblob import TextBlob as blob
import time
from collections import Counter
from nltk import tokenize

"""
----------------------------------------------------------------------------------------------------------------------
takes string-type HTML output and returns it as a BeautifulSoup object
"""
class CreateSoup:

    def __init__(self, content):

        self.content = content
        self.soup = None
        self.make_soup_object()

    # main method that type casts the string input to BeautifulSoup-type output
    def make_soup_object(self):

        self.soup = soup(self.content, 'html.parser')
        return self.soup
