#!/usr/bin/env python
################################################
#    Title: Reddit Crawler                     #
#    Author: Guillem Nicolau Alomar Sitjes     #
#    Date: September 1st, 2017                 #
#    Code version: 0.1                         #
#    Availability: Public                      #
################################################
import argparse
import urllib
import urllib2
import logging
import json
import dateutil.parser
from data_processing.data_processing import ProcessData

GET, POST = range(2)

logging.basicConfig(filename='reddit_crawler.log', level=logging.DEBUG)

def clean_screen():
    # Method called to do a 'clear', just for application visualization purposes
    print(chr(27) + "[2J")


def message_output():
    # Print method for the first message
    print "This is an application that obtains statistics about the first n pages of a given subreddit"


def decode_date(d):
    """
    The server sent us a date in the ISO format. Convert it to a datetime
    python object.
    """
    return dateutil.parser.parse(d)


def retrieve_data(subreddit, pages):
    """
    For each page in the first n pages of a given subreddit, store its data
    in the RestAPI DB.
    """
    logging.debug('retrieve_data method called with parameters:' +
                  str(subreddit) + ", " +
                  str(pages))
    try:
        get_response("fetch_subreddit", {"chosen_subreddit": subreddit, "num_pages": pages}, method=POST)
    except Exception as e:
        print "e:", e


def get_score_ranking(my_processor):
    """
    Show the top10 pages, by points
    """
    logging.debug('get_score_ranking method called with parameters:' +
                  str(my_processor))
    print "---------- Top 10 pages by score ----------"
    try:
        res = json.loads(get_response("get_score_ranking", {}, method=GET))
        for ind, entry in enumerate(my_processor.sort_by_score(res['result'])):
            print "Top " + str(ind + 1) + ": " + " Score: " + str(entry[0]) + " Title: " + str(entry[1])
            if ind + 1 == 10:
                break
    except Exception as e:
        print "e:", e


def get_discussion_ranking(my_processor):
    """
    Show the top10 pages, by comments
    """
    logging.debug('get_discussion_ranking method called with parameters:' +
                  str(my_processor))
    print "---------- Top 10 pages by comments ----------"
    try:
        res = json.loads(get_response("get_discussion_ranking", {}, method=GET))
        for ind, entry in enumerate(my_processor.sort_by_comments(res['result'])):
            print "Top " + str(ind + 1) + ": " + " Comments: " + str(entry[0]) + " Title: " + str(entry[1])
            if ind + 1 == 10:
                break
    except Exception as e:
        print "e:", e


def get_top_users_by_submissions_score(subreddit, my_processor):
    """
    Show the top10 users, by submission score
    """
    logging.debug('get_discussion_ranking method called with parameters:' +
                  str(my_processor))
    print "---------- Top 10 submitters by submissions score ----------"
    try:
        res = json.loads(get_response("get_top_users_by_submissions_score", {"chosen_subreddit": subreddit}, method=GET))
        for ind, entry in enumerate(my_processor.sort_authors_by_submission_score(res['result'])):
            print "Top " + str(ind + 1) + ": " + " Submissions score: " + str(entry[0]) + " Author: " + str(entry[1])
            if ind + 1 == 10:
                break
    except Exception as e:
        print "e:", e


def get_top_users_by_submissions(subreddit, my_processor):
    """
    Show the top10 users, by number of submissions
    """
    logging.debug('get_discussion_ranking method called with parameters:' +
                  str(my_processor))
    print "---------- Top 10 submitters by submissions ----------"
    try:
        res = json.loads(get_response("get_top_users_by_submissions", {"chosen_subreddit": subreddit}, method=GET))
        for ind, entry in enumerate(my_processor.sort_authors_by_submissions(res['result'])):
            print "Top " + str(ind + 1) + ": " + " Submissions: " + str(entry[0]) + " Author: " + str(entry[1])
            if ind + 1 == 10:
                break
    except Exception as e:
        print "e:", e


def get_top_users_by_score(subreddit, my_processor):
    """
    Show the top10 users, by comments score
    """
    logging.debug('get_discussion_ranking method called with parameters:' +
                  str(my_processor))
    print "---------- Top 10 commenters by score ----------"
    try:
        res = json.loads(get_response("get_top_users_by_comments_score", {"chosen_subreddit": subreddit}, method=GET))
        for ind, entry in enumerate(my_processor.sort_authors_by_score(res['result'])):
            print "Top " + str(ind + 1) + ": " + " Score: " + str(entry[0]) + " Author: " + str(entry[1])
            if ind + 1 == 10:
                break
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
                        help="Retrieve data and store it in DB", default=True)
    parser.add_argument('--specify-subreddit', action="store", dest="subreddit",
                        help="Specify the subreddit from where to fetch", default='Python')
    parser.add_argument('--specify-pages', action="store", dest="pages",
                        help="Specify the num of pages to fetch", default=20)

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    chosen_subreddit = args.subreddit
    num_pages = int(args.pages)

    if args.add_data:
        # Connect to the crawler through the RestAPI and make it store the subreddit data into the DB
        retrieve_data(chosen_subreddit, num_pages)

    processor = ProcessData()
    # GOALS
    # Connect to the RestAPI in order to obtain some statistics from the DB stored data
    get_score_ranking(processor)
    get_discussion_ranking(processor)

    # BONUS
    get_top_users_by_submissions_score(chosen_subreddit, processor)
    get_top_users_by_submissions(chosen_subreddit, processor)
    get_top_users_by_score(chosen_subreddit, processor)
    get_karma_stats()
