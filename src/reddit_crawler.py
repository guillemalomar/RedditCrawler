'''
/***********************************************
*    Title: Reddit Crawler                     *
*    Author: Guillem Nicolau Alomar Sitjes     *
*    Date: September 1st, 2017                 *
*    Code version: 0.1                         *
*    Availability: Public                      *
***********************************************/
'''
import argparse
import urllib
import urllib2

import dateutil.parser

# from rest_api.rest_api import import RestAPI

GET, POST = range(2)

# Method called to do a 'clear', just for application visualization purposes
def clean_screen():
    print(chr(27) + "[2J")


# Print method for the first message
def message_output():
    print "This is an application to That obtains the first n pages of a given subreddit,\n" \
          "To quit the application, insert \"exit\""


def decode_date(d):
    """
    The server sent us a date in the ISO format. Convert it to a datetime
    python object.
    """
    return dateutil.parser.parse(d)


def retrieve_data(subreddit, pages):
    """
    For each play listed above, first add the necessary metadata: channels,
    performers, songs, then the actual plays. Note that the metadata is posted
    more than once: if the data already exists on the server, it shouldn't be
    added again.
    """
    try:
        get_response("fetch_subreddit", {"chosen_subreddit": subreddit, "num_pages": pages}, method=POST)
    except Exception as e:
        print "e:", e


def get_score_ranking():
    try:
        get_response("get_score_ranking", {}, method=GET)
    except Exception as e:
        print "e:", e


def get_discussion_ranking():
    try:
        get_response("get_discussion_ranking", {}, method=GET)
    except Exception as e:
        print "e:", e


def get_top_users():
    try:
        get_response("get_top_users", {}, method=GET)
    except Exception as e:
        print "e:", e


def get_karma_stats():
    try:
        get_response("get_karma_stats", {}, method=GET)
    except Exception as e:
        print "e:", e


def get_response(fct, data, method=GET):
    """
    Performs the query to the server and returns a string containing the
    response.
    """
    assert(method in (GET, POST))
    url = 'http://%s:%s/%s' % (hostname, port, fct)
    if method == GET:
        req = urllib2.Request('%s?%s' % (url, urllib.urlencode(data)))
    elif method == POST:
        req = urllib2.Request(url, urllib.urlencode(data))
    response = urllib2.urlopen(req)
    return response.read()


# Main method
if __name__ == "__main__":
    clean_screen()
    message_output()

    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('-H', action="store", dest="hostname",
                        default="localhost", type=str)
    parser.add_argument('-P', action="store", dest="port",
                        default=8080, type=int)
    parser.add_argument('--add-data', action="store_true", dest="add_data",
                        help=("Retrieve data and store it in DB"), default=True)
    parser.add_argument('--specify-subreddit', action="store", dest="subreddit",
                        help=("Specify the subreddit from where to fetch"), default='Python')
    parser.add_argument('--specify-pages', action="store", dest="pages",
                        help=("Specify the num of pages to fetch"), default=10)

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    chosen_subreddit = args.subreddit
    num_pages = args.pages

    if args.add_data:
        # Connect to the crawler through the RestAPI and make it store the subreddit data into the DB
        retrieve_data(chosen_subreddit, num_pages)
        print "All data retrieved."

    # GOALS
    # Connect to the RestAPI in order to obtain some statistics from the DB stored data
    get_score_ranking()
    get_discussion_ranking()

    # BONUS
    get_top_users()
    get_karma_stats()