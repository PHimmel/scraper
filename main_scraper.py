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

from bs4 import BeautifulSoup as soup
import urllib
import urllib.request
import urllib.error
import re
from textblob import TextBlob as blob
import time
from collections import Counter
from nltk import tokenize


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

class Search(object):

    def __init__(self):

        self.search = None

        # starts the main method
        self.request_search_parameters()

    """
    request_search_parameters(self) requests user input to initialize the program
    """

    def request_search_parameters(self):

        # ask for search keyword/s
        self.search = input("What would you like to search for?\n")

        # echos the input for confirmation
        print(self.search + ", is what will be searched for.\n")

        # modify the string so it is 1. delimited by outer spaces
        #                            2. all in lowercase
        self.search = ' ' + self.search.casefold() + ' '

"""
----------------------------------------------------------------------------------------------------------------------
this class' purpose is 1. to create communication with the included news sites
        `              2. to run the Search() class' output against the main page content
"""

class NewsOutlets(object):

    # makes an empty list, as a class attribute, to store the pages titles
    yahoo_title_list = []

    # makes an empty list, as a class attribute, to store the full title data
    yahoo_full_data_list = []

    def __init__(self, search):

        # creates instance attribute that copies the value from Search() class

        self.search = search
        self.link = None
        self.title = None
        self.title_list = []
        self.matched_titles = []
        self.link_list = []
        self.articleNumber = None

        # starts the yahoo session by creating an instance variable of the class that uses urllib to create a session
        yahoo = HttpSession("https://news.yahoo.com")

        # creates a local instance attribute that passes along the raw HTML output from the previous variable into
        # the classes that transforms it into a BeautifulSoup object
        self.soup = CreateSoup(yahoo.read_contents) # -> to access the local attribute that holds the value
                                                  # self.soup.soup must be used

        # begins a chain of three methods that ultimately return usable links
        self.isolate_and_append_soup_titles()

    """
this method 1. separates the news articles' title info from the page
            2. takes the title string and lowers its case
            3. adds each processed title to the corresponding class attribute
    """
    def isolate_and_append_soup_titles(self):

        # crates a variable that contains a soup object with the raw data associated with each title
        soup_titles_only = self.soup.soup('a', class_='Fw(b)') # -> referencing the Soup class attribute

        # makes a loop that interates over the contents of the previous variable to isolate each title
        for titles in soup_titles_only:

            # adds the full title data to the appropriate class list
            NewsOutlets.yahoo_full_data_list.append(titles)

            # 1. the title string info is separated from the rest of the data
            # 2. the string has its case lowered
            # 3. it is added to the class attribute title list
            NewsOutlets.yahoo_title_list.append(titles.text.casefold())

        return self.search_soup_against_query()

    """
    this method searches the class attribute list of titles for ones that contain the specific
    search keyword/s
    """

    def search_soup_against_query(self):

        # interates over the title lists contents and creates an index positional variable
        for index, titles in enumerate(NewsOutlets.yahoo_title_list):

            # checks if the space-modified search query is present or if whitespace stripped search query is present
            if re.search(self.search.strip(), titles) or re.search(self.search, titles):
                if titles in self.matched_titles:
                    continue

                ### this statement copies the class attribute list value into instance list ###
                self.matched_titles.append(NewsOutlets.yahoo_full_data_list[index])

        # ends the method with a call to the next method in the sequence
        return self.extract_article_link()

    """
    this method pulls the unique part of the articles url address from the original HTML
    it then concatenates it with the base url to form a functioning url
    """

    def extract_article_link(self):

        # this conditional checks to find out if there is any matching results
        # if none are found then it returns to the the Main class, primary method

        if len(self.matched_titles) == 0:

            print("No articles found matching the search criteria.\n")

            # begins process all over again
            return Main().run_main_method

        # iterates over each title in the the list of matches
        for full_data in self.matched_titles:

            # prints the raw HTML code for each matched title
            self.title = full_data.text

            # takes the current title and adds it to a list (with same index position as the list list)
            self.title_list.append(self.title)

            # creates a variable that holds the unique part of the article address from the HTML code
            partial_link = full_data.get('href')

            # assigns the instance attribute to hold the working link
            self.link = 'https://www.news.yahoo.com' + partial_link

            # adds link to the master list
            self.link_list.append(self.link)

        # after both lists have been successfully created - then instance(with full list attributes)
        # is passed to the final step - to be converted into individual objects of the following, required class
        self.create_article_processing_object_with_self()

    """
    this method creates an ArticleProcessing object then passes its return value for the
    creation of a ReturnArticleData object. It does this individually for each article
    with the help of the for-loop
    """
    def create_article_processing_object_with_self(self):

        # creates a counter variable to retrieve the relevant title from its index position
        for index, link in enumerate(self.link_list):

            # these two statements set the instance attributes equal to those taken from the list contents
            self.link = link
            self.title = self.title_list[index]

            # this sets the artNum attribute to that of the index position and then casts it as a string to
            # concatenate it (with additional spaces) to the title
            self.articleNumber = index
            self.title = str(self.articleNumber + 1) + '.    ' + self.title

            # RAD object is created with the return of AP object    # these are the required attributes to create an AP object below

            ReturnArticleData(ArticleProcessing(self.link, self.title, self.link_list))


"""
----------------------------------------------------------------------------------------------------------------------
This class will take the raw articles then:
                                           1. break the total article in its smallest elements
                                           2. extract insightful information from those elements
                                           3. pass it on to the final stage, returning the output
"""
class ArticleProcessing(object):

    def __init__(self, link, title, link_list):
        self.link_list = link_list
        self.title = title
        self.link = link
        self.raw_site_contents = None
        self.article = None
        self.tokens = []
        self.sentiment = []
        self.blob = None
        self.mostCommon = []

     #   self.separate_link_list_and_process_individually()
        # instance method sequence
        self.main()
      #  self.mostCommon = []

    """
    this method organizes the required sub-methods
    """
    def main(self):

        # connects to internet, goes to article URL then makes a soup object from it
        self.establish_http_session()

        # textblob analysis
        self.textblob_analysis()

        # sets attribute to return value of method
        self.mostCommon = self.make_most_common_words()

    """
    organizes sub-methods needed for textblob analysis
    """
    def textblob_analysis(self):

        # transform
        self.make_textblob_object()

        # analyze full sentiment
        self.textblob_sentiment_analysis()

        # create tokens
        self.tokenize_words()

        # filter said tokens
        self.filter_tokenized_words()

    """
    creates an instance variable of the HTTP class to get raw HTML article data
    passes it into following method
    """
    def establish_http_session(self):

        self.raw_site_contents = HttpSession(self.link)

        return self.make_soup()

    """
    creates instance attribute of the CreateSoup class whilst sending in the raw HTML data
    """
    def make_soup(self):

        self.article = CreateSoup(self.raw_site_contents.read_contents) #  -> referring to separate class instance object attribute

        return self.article

    """

    """
    def extract_text_from_soup(self):

        pass
    """
    this method transforms the article beautiful soup object into a textblob object to use for processing
    """

    def make_textblob_object(self):

        # assigns the local attribute to the string-type converted BeautifulSoup object

        ### MUST MAKE SEPARATE METHOD FOR TEXT EXTRACTION AND STRING CONVERSION ### THIS IS MY CURRENT LOCATION TO WORK ON !!!!

        self.blob = blob(str(self.article.soup.text))


    """
    this method uses the textblob sentiment analysis tool to discern:
    1. Polarity (-1, 1) -1 -> negative, 1 -> positive
    2. Subjectivity (0, 1) 0 -> objective, 1 -> subjective
    """

    def textblob_sentiment_analysis(self):

        ### this adds the overall article sentiment to index 0 ###
        self.sentiment.append(self.blob.sentiment)

        # this loop iterates over each line within the article and assigns it a sentiment value
        # it then adds those individual values to the empty sentiment list
        for sentences in self.blob.split("."): # this function call results in a list consisting of strings separated
                                               # by a period
            sentence_sentiment = blob(sentences).sentiment
            self.sentiment.append(sentence_sentiment)

    """
    turns the sentences within the article into individual word tokens
    """

    def tokenize_words(self):

        # assigns the local attribute to the result of the tokens function call on the blob object
        self.tokens = self.blob.tokens


    """
    applies a filter to words tokens to remove irrelevant values
    """

    def filter_tokenized_words(self):
        pass

    """
    makes a list of the most common words from the token list
    """
    def make_most_common_words(self):

        return Counter(self.tokens).most_common()
    """
    takes the list of tokenized words and make a frequency distribution out of them
    """
    def make_frequency_distribution(self):

        pass


"""
----------------------------------------------------------------------------------------------------------------------
This class will take the processed info then: 1. save information of value to a .txt file
                                              2. upload the information to a SQL database
                                              3. print out the end final output to the monitor (including a graph)

        !!! ALL PRINTED OUTPUT MUST ULTIMATELY EMANATE FROM THIS CLASS !!!

"""

class ReturnArticleData(object):

    # sets a class-scoped variable to the current date and time
    now = (time.strftime('%a, %d %b %Y %I:%M:%S %p'))

    def __init__(self, data):

        self.data = data

        # calls the main method
        self.main()

    """
    this method serves as a class main that will orchestrate the sequence of sub-method calls
    """
    def main(self):

        # saves the gathered and processed data to a local txt file
        self.save_data_to_txt_file()

        ### FINAL RESULTS PRINTING ###

        # header
        self.print_the_results_header()

        # body
        self.print_body()

        # footer
        self.print_the_footer()

    """
    this method organizes the needed sub-methods within it
    """
    def print_body(self):

        # basic info
        self.print_title_and_url()

        # general sentiment
        self.print_overall_sentiment()

        # most common word list
        self.print_most_common_tokens()

    """
    save the data gathered in a local txt file
    """
    def save_data_to_txt_file(self):

        # accesses (or creates) the txt file
        with open('news.txt', 'w') as newsDoc:
                                               ### THIS IS CURRENTLY SET TO 'W' - AS SUCH, IT WILL ONLY RECORD ONE ARTICLE
                                               ### AT A TIME AND THEN WRITE OVER IT - CHANGE TO 'A' WHEN THE PROGRAM IS
                                               ### ULTIMATELY READY FOR REAL-TIME USE
            # writes the current date and time
            newsDoc.write(ReturnArticleData.now)

            # writes the articles title
            newsDoc.write(self.data.title)

            # inputs the full sentiment analysis
            newsDoc.write(str(self.data.sentiment))

            newsDoc.close()

    """
    prints the opening that segways into the actual results
    """
    def print_the_results_header(self):

        print("The results are:".center(150,'-'))

        # adds the current date and time
        print(ReturnArticleData.now)

        print()


    """
    a simple method to print out the basic info
    """
    def print_title_and_url(self):

        # outputs both the title and the link on two separate lines
        print(self.data.title)

        # adds additional whitespace to match the index and spacing of self.data.title
        print('      ' + self.data.link)

        print()

    """
    displays the overall article sentiment
    """
    def print_overall_sentiment(self):

        print("The overall article sentiment is:".center(75, "_"))

        print()

        # index 0 is reserved for the overall sentiments position - the rest are individual sentence sentiment
        print(self.data.sentiment[0])

        print()

    """
    prints the most common tokens found
    """
    def print_most_common_tokens(self):

        print("The most commonly found items are:".center(75, "_"))
        print()
        print(self.data.mostCommon)

        print()

    """
    prints the final closing for the output
    """
    def print_the_footer(self):

        print("End of results.".center(150, '-'))
        print("\n\n")





"""
----------------------------------------------------------------------------------------------------------------------
this class creates the HTTP session that is used:
                                                 1. initially to access the main pages full HTML
                                                 2. to access the individual articles that match the search query
"""
class HttpSession:

    def __init__(self, link):

        self.link = link
        self.read_contents = None
        self.initiate_session_connection()

    # the main method that creates the connection and then pulls its data into an attribute
    def initiate_session_connection(self):

        # makes a loop that removes overly-complicated error output from urllib
        # either urllib makes a successful connection or it fails (likely) due to a local
        # network issue
        while True:
            try:
                # sets the attribute to the string-type output of the HTML page data
                # includes the timeout parameter to limit waiting for likely error message
                self.read_contents = urllib.request.urlopen(self.link, timeout=10).read()
                break

            # this a urllib specific error code return that correlates to (often) an internet issue
            # (as opposed to a issue with the website itself)
            except urllib.error.URLError:
                print('TimeOut Error. Either too slow no no internet.')
                exit(1)

        # outputs the data in a usable format
        return self.read_contents

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
