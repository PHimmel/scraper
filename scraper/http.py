import urllib
import urllib.request
import urllib.error

"""
----------------------------------------------------------------------------------------------------------------------
Creates the HTTP session that is used:
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
