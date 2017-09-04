

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
