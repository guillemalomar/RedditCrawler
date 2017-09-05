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
import reddit_crawler_modes

GET, POST = range(2)


def clean_screen():
    # Method called to do a 'clear', just for application visualization purposes
    print(chr(27) + "[2J")


def message_header():
    # Print method for the header of the application
    print "******************************\n* Reddit Crawler Application *\n******************************"
    print "This is an application that obtains statistics of a given subreddit or reddit user"


def message_output():
    # Print method for the input modes
    show_modes()
    print " RETRIEVE - Fill database with subreddit data\n" + \
          " REFRESH  - Update database with subreddit data\n" + \
          " DELETE   - Delete all database data\n" + \
          " HELP     - Show the initial application message\n" + \
          " MODES    - Show the available modes\n" + \
          " EXIT     - Quit application"


def show_modes():
    # Print method for the available modes
    print "Available modes:"
    print " 1 - Get Pages by Score Ranking\n" + \
          " 2 - Get Pages by Comment Ranking\n" + \
          " 3 - Get Users by Submissions Score Ranking\n" + \
          " 4 - Get Users by Submissions Quantity\n" + \
          " 5 - Get Users by Comment Score\n" + \
          " 6 - Get Posts by User\n" + \
          " 7 - Get Comments by User\n" + \
          " 8 - Get Karma Stats from User"


def check_input(input_var):
    # Method to check if the user wants to finish the application
    if input_var.lower() == 'exit':
        print "The application will now end."
        clean_screen()
        raise SystemExit
    elif input_var.lower() == 'modes':
        show_modes()
        return False
    elif input_var.lower() == 'help':
        message_output()
        return False
    elif input_var.lower() == 'retrieve':
        return True
    elif input_var.lower() == 'delete':
        try:
            os.remove('src/rest_api/database/data/dbfile.sqlite')
            print "Database data removed"
        except Exception as e:
            print "Error trying to remove Database data:", e
        return False
    elif input_var.lower() == 'refresh':
        try:
            os.remove('src/rest_api/database/data/dbfile.sqlite')
            print "Database data removed"
        except Exception as e:
            print "Error trying to remove Database data:", e
        return True
    try:
        if int(input_var) not in range(0, 10):
            print "Please enter a valid mode."
            return False
    except:
        print "Please enter a valid mode."
        return False
    return True


# Main method
if __name__ == "__main__":
    clean_screen()
    message_header()
    message_output()

    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('-H', action="store", dest="hostname",
                        default="localhost", type=str)
    parser.add_argument('-P', action="store", dest="port",
                        default=8080, type=int)
    parser.add_argument('--specify-subreddit', action="store", dest="subreddit",
                        help="Specify the subreddit from where to fetch", default='Python')
    parser.add_argument('--specify-pages', action="store", dest="pages",
                        help="Specify the num of pages to fetch", default=100)
    parser.add_argument('--specify-user', action="store", dest="username",
                        help="Specify the name of the username to analyze", default='guillemnicolau')

    args = parser.parse_args()
    hostname = args.hostname
    port = args.port
    chosen_subreddit = args.subreddit
    num_pages = int(args.pages)
    chose_username = args.username

    while True:
        correct_input = False
        while not correct_input:
            print "***************************"
            var = raw_input("Please, enter a new mode: ")
            correct_input = check_input(var)
        if var.lower() == 'refresh' or var.lower() == 'retrieve':
            reddit_crawler_modes.retrieve_data(chosen_subreddit, num_pages, hostname, port)
        elif int(var) == 1:
            reddit_crawler_modes.get_score_ranking(hostname, port)
        elif int(var) == 2:
            reddit_crawler_modes.get_discussion_ranking(hostname, port)
        elif int(var) == 3:
            reddit_crawler_modes.get_top_users_by_submissions_score(chosen_subreddit, hostname, port)
        elif int(var) == 4:
            reddit_crawler_modes.get_top_users_by_submissions(chosen_subreddit, hostname, port)
        elif int(var) == 5:
            reddit_crawler_modes.get_top_users_by_score(chosen_subreddit, hostname, port)
        elif int(var) == 6:
            reddit_crawler_modes.get_posts_by_user(chose_username, hostname, port)
        elif int(var) == 7:
            reddit_crawler_modes.get_comments_by_user(chose_username, hostname, port)
        elif int(var) == 8:
            reddit_crawler_modes.get_karma_stats(chose_username, hostname, port)
