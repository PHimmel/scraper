#from scraper.search import Search
#from scraper.search import NewsOutlets


"""
----------------------------------------------------------------------------------------------------------------------
the main class creates the structure of the order of sequence that the program will follow

it creates instances of the specific classes and then passes the output from them into the
following class
"""

class MainProcess:

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
        from scraper.search import Search
        from scraper.search import NewsOutlets
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
