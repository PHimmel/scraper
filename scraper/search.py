from bs4 import BeautifulSoup as soup
import re
from scraper.http import HttpSession
from scraper.soup import CreateSoup
from scraper.process import ArticleProcessing
from scraper.persist import ReturnArticleData

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
            return MainProcess().run_main_method

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
