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
import scraper.articles
from scraper.articles.search import Search
from scraper.articles.search import NewsOutlets


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


"""
----------------------------------------------------------------------------------------------------------------------
the main class creates the structure of the order of sequence that the program will follow

it creates instances of the specific classes and then passes the output from them into the
following class
"""

class Main:

    def __init__(self):

        self.run_main_method()

    """
    !!!!   THIS IS THE MAIN PROGRAM METHOD. IT INITIATES THE WHOLE PROCESS !!!!

    it creates an indefinite while-loop that begins the program from the start
    is used for three reasons:

    1. if no articles are found matching the search criteria
    2. if the user stops the program whilst it is running
    3. once the program have concluded it offers the user the option of searching again
    """

    def run_main_method(self):

        while True:

            try:

                start = Search()
                NewsOutlets(start.search)

                # runs at program conclusion, requests if repetition is desired
                self.should_it_run_again()
                self.run_main_method()

            # the error code that is activated when the user terminates a program during run-time
            except KeyboardInterrupt:

                self.should_it_run_again()

                print("Okay, will search again.\n\n\n")

    def should_it_run_again(self):

        to_continue = input('Would you like to search again?\n'
                            'input either \'yes\' to continue.\n')

        if 'yes' in to_continue:
            self.run_main_method()
        else:
            print('\nOkay, goodbye.\n')
            exit(0)


# outputs the basic information of the program only once upon its execution
print_program_introduction()

# creates a variable that is a member of the Main class that begins the execution of the program
beg = Main()
