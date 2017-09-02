'''
/***********************************************
*    Title: Reddit Crawler                     *
*    Author: Guillem Nicolau Alomar Sitjes     *
*    Date: September 1st, 2017                 *
*    Code version: 0.1                         *
*    Availability: Public                      *
***********************************************/
'''

# from crawler.crawler import Crawler
# from rest_api.rest_api import import RestAPI


# Method called to do a 'clear', just for application visualization purposes
def clean_screen():
    print(chr(27) + "[2J")


# Print method for the first message
def message_output():
    print "This is an application to That obtains the first n pages of a given subreddit,\n" \
          "To quit the application, insert \"exit\""


# Main method
if __name__ == "__main__":
    clean_screen()
    message_output()

    # Create a Database and start it

    # Create a Crawler
    # Make it save the data about the first n pages of a given subreddit into our database

    # Connect to the RestAPI in order to obtain some statistics from the DB stored data

    # Stop the database