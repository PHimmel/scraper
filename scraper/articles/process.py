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
