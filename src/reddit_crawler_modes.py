#!/usr/bin/env python
################################################
#    Title: Reddit Crawler                     #
#    Author: Guillem Nicolau Alomar Sitjes     #
#    Date: September 1st, 2017                 #
#    Code version: 0.1                         #
#    Availability: Public                      #
################################################
import urllib.request
import urllib.parse
try: #python3
    from urllib.request import urlopen
except: #python2
    from urllib2 import urlopen
import logging
import json
import re
from data_processing.data_processing import ProcessData
from timer import Timer

GET, POST = range(2)

logging.basicConfig(filename='logs/reddit_crawler.log', level=logging.DEBUG)
logging.getLogger("urllib").setLevel(logging.WARNING)


def retrieve_data(subreddit, pages, hostname, port):
    """
    For each page in the first n pages of a given subreddit, store its data
    in the RestAPI Database.
    :param subreddit: current subreddit
    :param pages: max num of pages
    :param hostname: server location
    :param port: server port
    :return:
    """
    logging.debug('retrieve_data method called with parameters:' +
                  str(subreddit) + ", " +
                  str(pages))
    my_timer = Timer()
    try:
        get_response("fetch_subreddit",
                     str('{"chosen_subreddit": ' + str(subreddit) + ', "num_pages": ' + str(pages) + '}').encode('utf-8'),
                     hostname,
                     port,
                     method=POST)
    except Exception as e:
        print("Error in retrieve_data:{}".format(e))
        logging.error('retrieve_data error: ' + str(e))
        raise e
        return False
    logging.debug('retrieve_data method total time:' + str(my_timer.finish()))
    return True

_reddit_url = re.compile('.*https://www.reddit.com/r/+.*')


def get_score_ranking(hostname, port):
    """
    Show the top10 pages, by points
    :param hostname: server location
    :param port: server port
    :return:
    """
    logging.debug('get_score_ranking method called')
    my_timer = Timer()
    print("------------------ TOP PAGES RANKINGS BY SCORE ------------------")
    try:
        res = json.loads(get_response("get_score_ranking",
                                      '{}'.encode('utf-8'),
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print("No results, database is probably empty")
        else:
            outside_pages = []
            comment_pages = []
            any_kind = []
            for ind, entry in enumerate(ProcessData.sort_by_score(res['result'])):
                m = _reddit_url.match(entry[2])
                if m is not None:
                    comment_pages.append((entry[0], entry[1], entry[2]))
                else:
                    outside_pages.append((entry[0], entry[1], entry[2]))
                any_kind.append((entry[0], entry[1], entry[2]))
            print("---------- Top pages rankings by score - Outside Links ----------")
            for ind, entry in enumerate(outside_pages):
                print("Top {} - Score: {}".format(ind+1, entry[0]))
                print("       Title: {}".format(entry[1]))
                print("       Link: {}".format(entry[2]))
                if ind + 1 == 10:
                    break
            print("---------- Top pages rankings by score - Comment Links ----------")
            for ind, entry in enumerate(comment_pages):
                print("Top {} - Score: {}".format(ind + 1, entry[0]))
                print("       Title: {}".format(entry[1]))
                print("       Link: {}".format(entry[2]))
                if ind + 1 == 10:
                    break
            print("---------- Top pages rankings by score - Any kind of Links ----------")
            for ind, entry in enumerate(any_kind):
                print("Top {} - Score: {}".format(ind + 1, entry[0]))
                print("       Title: {}".format(entry[1]))
                print("       Link: {}".format(entry[2]))
                if ind + 1 == 10:
                    break
    except Exception as e:
        print("Error in get_score_ranking:{}".format(e))
        logging.error('get_score_ranking error: ' + str(e))
        raise e
    logging.debug('get_score_ranking method total time:' + str(my_timer.finish()))


def get_discussion_ranking(hostname, port):
    """
    Show the top10 pages, by comments
    :param hostname: server location
    :param port: server port
    :return:
    """
    logging.debug('get_discussion_ranking method called')
    my_timer = Timer()
    print("---------- TOP PAGES RANKINGS BY COMMENTS SCORE ----------")
    outside_pages = []
    comment_pages = []
    any_kind = []
    try:
        res = json.loads(get_response("get_discussion_ranking",
                                      '{}'.encode('utf-8'),
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print("No results, database is probably empty")
        else:
            for ind, entry in enumerate(ProcessData.sort_by_comments(res['result'])):
                m = _reddit_url.match(entry[2])
                if m is not None:
                    comment_pages.append((entry[0], entry[1], entry[2]))
                else:
                    outside_pages.append((entry[0], entry[1], entry[2]))
                any_kind.append((entry[0], entry[1], entry[2]))
            print("---------- Top pages rankings by comments - Outside Links ----------")
            for ind, entry in enumerate(outside_pages):
                print("Top " + str(ind + 1) + " - Comments: " + str(entry[0]))
                print("       Title: " + str(entry[1]))
                print("       Link: " + str(entry[2]))
                if ind + 1 == 10:
                    break
            print("---------- Top pages rankings by comments - Comment Links ----------")
            for ind, entry in enumerate(comment_pages):
                print("Top " + str(ind + 1) + " - Comments: " + str(entry[0]))
                print("       Title: " + str(entry[1]))
                print("       Link: " + str(entry[2]))
                if ind + 1 == 10:
                    break
            print("---------- Top pages rankings by comments - Any kind of Links ----------")
            for ind, entry in enumerate(any_kind):
                print("Top " + str(ind + 1) + " - Comments: " + str(entry[0]))
                print("       Title: " + str(entry[1]))
                print("       Link: " + str(entry[2]))
                if ind + 1 == 10:
                    break
    except Exception as e:
        print("Error in get_discussion_ranking:", e)
        logging.error('get_discussion_ranking error: ' + str(e))
    logging.debug('get_discussion_ranking method total time:' + str(my_timer.finish()))


def get_top_users_by_submissions_score(subreddit, hostname, port):
    """
    Show the top10 users of a subreddit, by submission score
    :param subreddit: current subreddit
    :param hostname: server location
    :param port: server port
    :return:
    """
    logging.debug('get_top_users_by_submissions_score method called')
    my_timer = Timer()
    print("---------- Top Submitters ----------")
    try:
        res = json.loads(get_response("get_top_users_by_submissions_score",
                                      '{"chosen_subreddit": subreddit}'.encode('utf-8'),
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print("No results, database is probably empty")
        else:
            for ind, entry in enumerate(ProcessData.sort_authors_by_submission_score(res['result'])):
                print("Top " + str(ind + 1) + " - Submissions score: " + str(entry[0]) + " Author: " + str(entry[1]))
                if ind + 1 == 10:
                    break
    except Exception as e:
        print("Error in get_top_users_by_submissions_score:", e)
        logging.error('get_top_users_by_submissions_score error: ' + str(e))
    logging.debug('get_top_users_by_submissions_score method total time:' + str(my_timer.finish()))


def get_top_users_by_submissions(subreddit, hostname, port):
    """
    Show the top10 users of a subreddit, by submission score
    :param subreddit: current subreddit
    :param hostname: server location
    :param port: server port
    :return:
    """
    logging.debug('get_top_users_by_submissions method called')
    my_timer = Timer()
    print("---------- Most Active Users ----------")
    try:
        res = json.loads(get_response("get_top_users_by_submissions",
                                      '{"chosen_subreddit": subreddit}'.encode('utf-8'),
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print("No results, database is probably empty")
        else:
            for ind, entry in enumerate(ProcessData.sort_authors_by_submissions(res['result'])):
                print("Top " + str(ind + 1) + " - Submissions: " + str(entry[0]) + " Author: " + str(entry[1]))
                if ind + 1 == 10:
                    break
    except Exception as e:
        print("Error in get_top_users_by_submissions:", e)
        logging.error('get_top_users_by_submissions error: ' + str(e))
    logging.debug('get_top_users_by_submissions method total time:' + str(my_timer.finish()))


def get_top_users_by_score(subreddit, hostname, port):
    """
    Show the top10 users of a subreddit, by comments score
    :param subreddit: current subreddit
    :param hostname: server location
    :param port: server port
    :return:
    """
    logging.debug('get_top_users_by_score method called')
    my_timer = Timer()
    print("---------- Top commenters ----------")
    try:
        res = json.loads(get_response("get_top_users_by_comments_score",
                                      '{"chosen_subreddit": subreddit}'.encode('utf-8'),
                                      hostname,
                                      port,
                                      method=GET))
        for ind, entry in enumerate(ProcessData.sort_authors_by_score(res['result'])):
            print("Top " + str(ind + 1) + " -  Score: " + str(entry[0]) + " Author: " + str(entry[1]))
            if ind + 1 == 10:
                break
    except Exception as e:
        print("Error in get_top_users_by_score:", e)
        logging.error('get_top_users_by_score error: ' + str(e))
    logging.debug('get_top_users_by_score method total time:' + str(my_timer.finish()))


def get_posts_by_user(chosen_username, hostname, port):
    """
    Show the first 10 posts for a given users
    :param chosen_username: current username
    :param hostname: server location
    :param port: server port
    :return:
    """
    logging.debug('get_posts_by_user method called')
    my_timer = Timer()
    print("---------- Posts by the user " + str(chosen_username) + " ----------")
    try:
        res = json.loads(get_response("get_posts_by_user",
                                      '{"chosen_username": chosen_username}'.encode('utf-8'),
                                      hostname,
                                      port,
                                      method=GET))
        for ind, entry in enumerate(res['result']):
            print("Post " + str(ind + 1) + " - Title: " + str(entry['title']) + \
                  " Subreddit: " + str(entry['subreddit']))
            if ind + 1 == 10:
                break
    except Exception as e:
        print("Error in get_posts_by_user:", e)
        logging.error('get_posts_by_user error: ' + str(e))
    logging.debug('get_posts_by_user method total time:' + str(my_timer.finish()))


def get_comments_by_user(chosen_username, hostname, port):
    """
    Show the top10 users, by comments score
    :param chosen_username: current username
    :param hostname: server location
    :param port: server port
    :return:
    """
    logging.debug('get_comments_by_user method called')
    my_timer = Timer()
    print("---------- Comments by the user " + str(chosen_username) + " ----------")
    try:
        res = json.loads(get_response("get_comments_by_user",
                                      '{"chosen_username": chosen_username}'.encode('utf-8'),
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print("No results, database is probably empty")
        for ind, entry in enumerate(res['result']):
            print("Post " + str(ind + 1) + " - Comment: " + str(entry['comment']) + \
                  " Subreddit: " + str(entry['subreddit']))
            if ind + 1 == 10:
                break
    except Exception as e:
        print("Error in get_comments_by_user:", e)
        logging.error('get_comments_by_user error: ' + str(e))
    logging.debug('get_comments_by_user method total time:' + str(my_timer.finish()))


def get_karma_stats(chose_username, hostname, port):
    """
    Show the average karma of the comments for a given user
    :param chose_username: current username
    :param hostname: server location
    :param port: server port
    :return:
    """
    logging.debug('get_karma_stats method called')
    my_timer = Timer()
    print("---------- Karma statistics of the user " + str(chose_username) + " ----------")
    try:
        res = json.loads(get_response("get_karma_stats",
                                      '{"chosen_username": chose_username}'.encode('utf-8'),
                                      hostname,
                                      port,
                                      method=GET))
        if len(res['result']) == 0:
            print("No results, database is probably empty")
        print("Average_karma: " + str(res['result'][0]['avg_karma']))
    except Exception as e:
        print("Error in get_karma_stats:", e)
        logging.error('get_karma_stats error: ' + str(e))
    logging.debug('get_karma_stats method total time:' + str(my_timer.finish()))


def get_response(fct, data, hostname, port, method=GET):
    """
    Performs the query to the server and returns a string containing the
    response.
    :param fct: alias of the method to find in the RestAPI server
    :param data: input data of the RestAPI method
    :param hostname: server location
    :param port: server port
    :param method: type of RestAPI method (GET)
    :return: return RestAPI method output
    """
    assert(method in (GET, POST))
    url = 'http://%s:%s/%s' % (hostname, port, fct)
    print("url:  {}".format(url))
    print("data: {}".format(data))
    req = ''
    if method == GET:
        req = urlopen('%s?%s' % (url, data))
    elif method == POST:
        req = urlopen(url, data)
    return req.read()
