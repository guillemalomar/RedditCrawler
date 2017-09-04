

class ProcessData:
    def __init__(self):
        pass

    @staticmethod
    def sort_by_score(list_to_process):
        list_to_return = []
        for list_dict in list_to_process:
            list_to_return.append((list_dict['score'], list_dict['title']))
        sorted_list = sorted(list_to_return, key=lambda x: x[0], reverse=True)
        return sorted_list

    @staticmethod
    def sort_by_comments(list_to_process):
        list_to_return = []
        for list_dict in list_to_process:
            list_to_return.append((list_dict['num_comments'], list_dict['title']))
        sorted_list = sorted(list_to_return, key=lambda x: x[0], reverse=True)
        return sorted_list

    @staticmethod
    def sort_authors_by_score(list_to_process):
        list_to_return = []
        for list_dict in list_to_process:
            list_to_return.append((list_dict['score'], list_dict['author']))
        sorted_list = sorted(list_to_return, key=lambda x: x[0], reverse=True)
        return sorted_list

    @staticmethod
    def sort_authors_by_submission_score(list_to_process):
        list_to_return = []
        gathered_dict = {}
        for list_dict in list_to_process:
            gathered_dict[str(list_dict['submitter'])] = gathered_dict.get(str(list_dict['submitter']), 0) + list_dict['punctuation']
        for submitter, punctuation in gathered_dict.iteritems():
            list_to_return.append((punctuation, submitter))
        sorted_list = sorted(list_to_return, key=lambda x: x[0], reverse=True)
        return sorted_list

    @staticmethod
    def sort_authors_by_submissions(list_to_process):
        list_to_return = []
        gathered_dict = {}
        for list_dict in list_to_process:
            gathered_dict[str(list_dict['submitter'])] = gathered_dict.get(str(list_dict['submitter']), 0) + 1
        for submitter, submission in gathered_dict.iteritems():
            list_to_return.append((submission, submitter))
        sorted_list = sorted(list_to_return, key=lambda x: x[0], reverse=True)
        return sorted_list
