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
