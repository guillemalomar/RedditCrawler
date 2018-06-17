#!/usr/bin/env python
################################################
#    Title: Reddit Crawler                     #
#    Author: Guillem Nicolau Alomar Sitjes     #
#    Date: September 1st, 2017                 #
#    Code version: 0.1                         #
#    Availability: Public                      #
################################################
import argparse
import os
from reddit_crawler_modes import *
import logging
from settings import rest_api_log

GET, POST = range(2)

logging.basicConfig(filename=rest_api_log, level=logging.DEBUG)


def clean_screen():
    """
    Method called to do a 'clear', just for application visualization purposes
    :return:
    """
    print(chr(27) + "[2J")


def message_header():
    """
    Print method for the header of the application
    :return:
    """
    print("******************************\n* Reddit Crawler Application *\n******************************")
    print("This is an application that obtains statistics of a given subreddit or reddit user")


def show_modes():
    """
    Print method for the available data processing modes
    :return:
    """
    print("Available modes:")
    print(" 1 - Get Pages by Score Ranking\n" +
          " 2 - Get Pages by Comment Ranking\n" +
          " 3 - Get Users by Submissions Score Ranking\n" +
          " 4 - Get Users by Submissions Quantity\n" +
          " 5 - Get Users by Comment Score\n" +
          " 6 - Get Posts by User\n" +
          " 7 - Get Comments by User\n" +
          " 8 - Get Karma Stats from User")


def message_output():
    """
    Print method for all the available modes
    :return:
    """
    show_modes()
    print(" RETRIEVE - Fill database with subreddit data\n" +
          " REFRESH  - Update database with subreddit data\n" +
          " DELETE   - Delete all database data\n" +
          " HELP     - Show the initial application message\n" +
          " MODES    - Show the available modes\n" +
          " EXIT     - Quit application")


def check_input(input_var):
    """
    Method to check if the selected method is correct, and to exit if wanted
    :param input_var: user mode selected
    :return: True (Mode to execute) / False (Mode executed or incorrect)
    """
    if input_var.lower() == 'exit':
        print("The application will now end.")
        clean_screen()
        raise SystemExit
    elif input_var.lower() == 'modes':
        show_modes()
        return False
    elif input_var.lower() == 'help':
        message_output()
        return False
    elif input_var.lower() in ['retrieve', 'delete', 'refresh']:
        return True
    elif input_var not in ['1', '2', '3', '4', '5', '6', '7', '8']:
        print("Please enter a valid mode.")
        return False
    return True


# Main method
if __name__ == "__main__":
    clean_screen()

    # Arguments are taken from command line
    parser = argparse.ArgumentParser(description='Reddit Crawler Client',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--hostname', action="store", dest="hostname",
                        help="Hostname to connect to the server",
                        default="localhost", type=str)
    parser.add_argument('--port', action="store", dest="port",
                        help="Port to connect to the server",
                        default=8080, type=int)
    parser.add_argument('--subreddit', action="store", dest="subreddit",
                        help="Specify the subreddit from where to fetch", default='Python', type=str)
    parser.add_argument('--pages', action="store", dest="pages",
                        help="Specify the num of pages to fetch", default=100, type=int)
    parser.add_argument('--user', action="store", dest="username",
                        help="Specify the name of the username to analyze", default='guillemnicolau', type=str)

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    chosen_subreddit = args.subreddit
    num_pages = int(args.pages)
    chosen_username = args.username

    message_header()
    message_output()

    while True:
        correct_input = False
        while not correct_input:
            print("***************************")
            var = input("Please, enter a new mode: ")
            correct_input = check_input(var)
        if var.lower() == 'delete' or var.lower() == 'refresh':
            try:
                os.remove('src/rest_api/database/data/dbfile.sqlite')
                logging.debug('Database emptied')
                print('Database emptied')
            except OSError:
                logging.debug("Error trying to remove Database data: File doesn't exist")
                print("Error trying to remove Database data: File doesn't exist")
        if var.lower() == 'retrieve' or var.lower() == 'refresh':
            result = retrieve_data(hostname, port, chosen_subreddit, num_pages)
            if result:
                logging.debug('Database filled')
                print('Database filled')
            else:
                logging.debug('Database not filled')
                print('Database not filled')
        elif var == '1':
            get_score_ranking(hostname, port, chosen_subreddit)
        elif var == '2':
            get_discussion_ranking(hostname, port, chosen_subreddit)
        elif var == '3':
            get_top_users_by_submissions_score(hostname, port, chosen_subreddit)
        elif var == '4':
            get_top_users_by_submissions(hostname, port, chosen_subreddit)
        elif var == '5':
            get_top_users_by_score(hostname, port, chosen_subreddit)
        elif var == '6':
            get_posts_by_user(hostname, port, chosen_username)
        elif var == '7':
            get_comments_by_user(hostname, port, chosen_username)
        elif var == '8':
            get_karma_stats(hostname, port, chosen_username)
