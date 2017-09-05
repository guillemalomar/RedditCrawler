#!/usr/bin/env python
################################################
#    Title: Reddit Crawler                     #
#    Author: Guillem Nicolau Alomar Sitjes     #
#    Date: September 1st, 2017                 #
#    Code version: 0.1                         #
#    Availability: Public                      #
################################################


class ProcessData:
    def __init__(self):
        pass

    @staticmethod
    def sort_by_score(list_to_process):
        """
        Method needed by mode 1
        :param list_to_process: unsorted list of dicts of score, title and url
        :return: sorted list by score
        """
        list_to_return = []
        for list_dict in list_to_process:
            list_to_return.append((list_dict['score'], list_dict['title'], list_dict['url']))
        sorted_list = sorted(list_to_return, key=lambda x: x[0], reverse=True)
        return sorted_list

    @staticmethod
    def sort_by_comments(list_to_process):
        """
        Method needed by mode 2
        :param list_to_process: unsorted list of dicts of num_comments, title and url
        :return: sorted list by comments
        """
        list_to_return = []
        for list_dict in list_to_process:
            list_to_return.append((list_dict['num_comments'], list_dict['title'], list_dict['url']))
        sorted_list = sorted(list_to_return, key=lambda x: x[0], reverse=True)
        return sorted_list

    @staticmethod
    def sort_authors_by_submission_score(list_to_process):
        """
        Method needed by mode 3
        :param list_to_process: unsorted list of dicts of authors and submission score
        :return: sorted list of authors by submission score
        """
        list_to_return = []
        gathered_dict = {}
        for list_dict in list_to_process:
            gathered_dict[str(list_dict['submitter'])] = gathered_dict.get(str(list_dict['submitter']), 0) + \
                                                         list_dict['punctuation']
        for submitter, punctuation in gathered_dict.iteritems():
            list_to_return.append((punctuation, submitter))
        sorted_list = sorted(list_to_return, key=lambda x: x[0], reverse=True)
        return sorted_list

    @staticmethod
    def sort_authors_by_submissions(list_to_process):
        """
        Method needed by mode 4
        :param list_to_process: unsorted list of dicts of submitter and title
        :return: sorted list of authors by submission quantity
        """
        list_to_return = []
        gathered_dict = {}
        for list_dict in list_to_process:
            gathered_dict[str(list_dict['submitter'])] = gathered_dict.get(str(list_dict['submitter']), 0) + 1
        for submitter, submission in gathered_dict.iteritems():
            list_to_return.append((submission, submitter))
        sorted_list = sorted(list_to_return, key=lambda x: x[0], reverse=True)
        return sorted_list

    @staticmethod
    def sort_authors_by_score(list_to_process):
        """
        Method needed by mode 5
        :param list_to_process: unsorted list of author, body and comment score
        :return: sorted list of authors by comment score
        """
        list_to_return = []
        for list_dict in list_to_process:
            list_to_return.append((list_dict['score'], list_dict['author']))
        sorted_list = sorted(list_to_return, key=lambda x: x[0], reverse=True)
        return sorted_list
