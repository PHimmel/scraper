"""
Program description:

This is a top-down development approach to the initial project that will be
in accordance with the created structure chart.

The end goal is to produce output that offers both the original text as well
as analysis of the aforementioned documents.

    *** ADDITIONAL GOALS ***

    1. reduce/ameliorate dependencies by:

            using the fewest libraries as possible
            using newest/most supported libraries
            factoring in contingencies for said libraries and their potential failures

    2. decomposition does not end with functions, decompose statements to their most simple
    form possible (even at the cost of additional lines of code)

"""

"""
Required dependencies:

urllib/selenium -> to establish HTTP sessions with the source sites

bs4/re -> for parsing HTML documents to locate the searched input

time -> to delay program operations (i.e. output)

textblob -> a tool for text analysis

"""

#from . import articles
from bs4 import BeautifulSoup as soup
import urllib
import urllib.request
import urllib.error
import re
from textblob import TextBlob as blob
import time
from collections import Counter
from nltk import tokenize
from scraper.main import Main


"""
this ***static function*** prints a program introduction to the user specifying what the program does exactly such as:
1. the news sources that it will search through
2. the analytics that will be performed on the resulting data
3. the ultimate output of the program
it is only used once upon the initialization of the program
"""
def print_program_introduction():

    print('''
I will parse the front page of Yahoo News to look to find your search keyword/s.
Then will convert it in tokens and analyze the significance of them.
Finally, I shall return:
         1. the basic article information
         2. The corresponding sentiment values
         3. The tokens that comprise the article
         ''')

"""
----------------------------------------------------------------------------------------------------------------------
this class initiates the program with the search input from the user
"""


# outputs the basic information of the program only once upon its execution
print_program_introduction()

# creates a variable that is a member of the Main class that begins the execution of the program
beg = Main()
