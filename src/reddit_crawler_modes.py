#!/usr/bin/env python
################################################
#    Title: Reddit Crawler                     #
#    Author: Guillem Nicolau Alomar Sitjes     #
#    Date: September 1st, 2017                 #
#    Code version: 0.1                         #
#    Availability: Public                      #
################################################
import urllib
import urllib2
import logging
import json
import re
from data_processing.data_processing import ProcessData

GET, POST = range(2)

logging.basicConfig(filename='reddit_crawler.log', level=logging.DEBUG)


def retrieve_data(subreddit, pages, hostname, port):
    """
    For each page in the first n pages of a given subreddit, store its data
    in the RestAPI Database.
    """
    logging.debug('retrieve_data method called with parameters:' +
                  str(subreddit) + ", " +
                  str(pages))
    try:
        get_response("fetch_subreddit",
                     {"chosen_subreddit": subreddit, "num_pages": pages},
                     hostname,
                     port,
                     method=POST)
        print "Database updated"
    except Exception as e:
        print "e:", e

_reddit_url = re.compile('.*https://www.reddit.com/r/+.*')


def get_score_ranking(hostname, port):
    """
    Show the top10 pages, by points
    """
    logging.debug('get_score_ranking method called')
    print "------------------ TOP PAGES RANKINGS BY SCORE ------------------"
    outside_pages = []
    comment_pages = []
    any_kind = []
    try:
        res = json.loads(get_response("get_score_ranking",
                                      {},
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        else:
            for ind, entry in enumerate(ProcessData.sort_by_score(res['result'])):
                m = _reddit_url.match(entry[2])
                if m is not None:
                    comment_pages.append((entry[0], entry[1], entry[2]))
                else:
                    outside_pages.append((entry[0], entry[1], entry[2]))
                any_kind.append((entry[0], entry[1], entry[2]))
            print "---------- Top pages rankings by score - Outside Links ----------"
            for ind, entry in enumerate(outside_pages):
                print "Top " + str(ind + 1) + " - Score: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
            print "---------- Top pages rankings by score - Comment Links ----------"
            for ind, entry in enumerate(comment_pages):
                print "Top " + str(ind + 1) + " - Score: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
            print "---------- Top pages rankings by score - Any kind of Links ----------"
            for ind, entry in enumerate(any_kind):
                print "Top " + str(ind + 1) + " - Score: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
    except Exception as e:
        print "e:", e


def get_discussion_ranking(hostname, port):
    """
    Show the top10 pages, by comments
    """
    logging.debug('get_discussion_ranking method called')
    print "---------- TOP PAGES RANKINGS BY COMMENTS SCORE ----------"
    outside_pages = []
    comment_pages = []
    any_kind = []
    try:
        res = json.loads(get_response("get_discussion_ranking",
                                      {},
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        else:
            for ind, entry in enumerate(ProcessData.sort_by_comments(res['result'])):
                m = _reddit_url.match(entry[2])
                if m is not None:
                    comment_pages.append((entry[0], entry[1], entry[2]))
                else:
                    outside_pages.append((entry[0], entry[1], entry[2]))
                any_kind.append((entry[0], entry[1], entry[2]))
            print "---------- Top pages rankings by comments - Outside Links ----------"
            for ind, entry in enumerate(outside_pages):
                print "Top " + str(ind + 1) + " - Comments: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
            print "---------- Top pages rankings by comments - Comment Links ----------"
            for ind, entry in enumerate(comment_pages):
                print "Top " + str(ind + 1) + " - Comments: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
            print "---------- Top pages rankings by comments - Any kind of Links ----------"
            for ind, entry in enumerate(any_kind):
                print "Top " + str(ind + 1) + " - Comments: " + str(entry[0])
                print "       Title: " + str(entry[1])
                print "       Link: " + str(entry[2])
                if ind + 1 == 10:
                    break
    except Exception as e:
        print "e:", e


def get_top_users_by_submissions_score(subreddit, hostname, port):
    """
    Show the top10 users of a subreddit, by submission score
    """
    logging.debug('get_top_users_by_submissions_score method called')
    print "---------- Top Submitters ----------"
    try:
        res = json.loads(get_response("get_top_users_by_submissions_score",
                                      {"chosen_subreddit": subreddit},
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        else:
            for ind, entry in enumerate(ProcessData.sort_authors_by_submission_score(res['result'])):
                print "Top " + str(ind + 1) + " - Submissions score: " + str(entry[0]) + " Author: " + str(entry[1])
                if ind + 1 == 10:
                    break
    except Exception as e:
        print "e:", e


def get_top_users_by_submissions(subreddit, hostname, port):
    """
    Show the top10 users of a subreddit, by number of submissions
    """
    logging.debug('get_top_users_by_submissions method called')
    print "---------- Most Active Users ----------"
    try:
        res = json.loads(get_response("get_top_users_by_submissions",
                                      {"chosen_subreddit": subreddit},
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        else:
            for ind, entry in enumerate(ProcessData.sort_authors_by_submissions(res['result'])):
                print "Top " + str(ind + 1) + " - Submissions: " + str(entry[0]) + " Author: " + str(entry[1])
                if ind + 1 == 10:
                    break
    except Exception as e:
        print "e:", e


def get_top_users_by_score(subreddit, hostname, port):
    """
    Show the top10 users of a subreddit, by comments score
    """
    logging.debug('get_top_users_by_score method called')
    print "---------- Top commenters ----------"
    try:
        res = json.loads(get_response("get_top_users_by_comments_score",
                                      {"chosen_subreddit": subreddit},
                                      hostname,
                                      port,
                                      method=GET))
        for ind, entry in enumerate(ProcessData.sort_authors_by_score(res['result'])):
            print "Top " + str(ind + 1) + " -  Score: " + str(entry[0]) + " Author: " + str(entry[1])
            if ind + 1 == 10:
                break
    except Exception as e:
        print "e:", e


def get_posts_by_user(chosen_username, hostname, port):
    """
    Show the first 10 posts for a given users
    """
    logging.debug('get_posts_by_user method called')
    print "---------- Posts by the user " + str(chosen_username) + " ----------"
    try:
        res = json.loads(get_response("get_posts_by_user",
                                      {"chosen_username": chosen_username},
                                      hostname,
                                      port,
                                      method=GET))
        for ind, entry in enumerate(res['result']):
            print "Post " + str(ind + 1) + " - Title: " + str(entry['title']) + \
                  " Subreddit: " + str(entry['subreddit'])
            if ind + 1 == 10:
                break
    except Exception as e:
        print "e:", e


def get_comments_by_user(chosen_username, hostname, port):
    """
    Show the top10 users, by comments score
    """
    logging.debug('get_comments_by_user method called')
    print "---------- Comments by the user " + str(chosen_username) + " ----------"
    try:
        res = json.loads(get_response("get_comments_by_user",
                                      {"chosen_username": chosen_username},
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        for ind, entry in enumerate(res['result']):
            print "Post " + str(ind + 1) + " - Comment: " + str(entry['comment']) + \
                  " Subreddit: " + str(entry['subreddit'])
            if ind + 1 == 10:
                break
    except Exception as e:
        print "e:", e


def get_karma_stats(chose_username, hostname, port):
    """
    Show the average karma of the comments for a given user
    """
    logging.debug('get_karma_stats method called')
    print "---------- Karma statistics of the user " + str(chose_username) + " ----------"
    try:
        res = json.loads(get_response("get_karma_stats",
                                      {"chosen_username": chose_username},
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print "No results, database is probably empty"
        print "Average_karma: " + str(res['result'][0]['avg_karma'])
    except Exception as e:
        print "e:", e


def get_response(fct, data, hostname, port, method=GET):
    """
    Performs the query to the server and returns a string containing the
    response.
    """
    assert(method in (GET, POST))
    url = 'http://%s:%s/%s' % (hostname, port, fct)
    req = ''
    if method == GET:
        req = urllib2.Request('%s?%s' % (url, urllib.urlencode(data)))
    elif method == POST:
        req = urllib2.Request(url, urllib.urlencode(data))
    response = urllib2.urlopen(req)
    return response.read()
