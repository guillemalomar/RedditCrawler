import unittest
from data_processing import ProcessData


class DataProcessing_Tests(unittest.TestCase):

    def test_sort_by_score(self):
        result = ProcessData.sort_by_score([{'score': 1, 'title': 'score1', 'url': 'url_score1'},
                                            {'score': 3, 'title': 'score3', 'url': 'url_score3'},
                                            {'score': 2, 'title': 'score2', 'url': 'url_score2'}])
        self.assertEquals(3, result[0][0])
        self.assertEquals(2, result[1][0])
        self.assertEquals(1, result[2][0])

    def test_sort_by_comments(self):
        result = ProcessData.sort_by_comments([{'num_comments': 2, 'title': 'score1', 'url': 'url_score1'},
                                               {'num_comments': 3, 'title': 'score3', 'url': 'url_score3'},
                                               {'num_comments': 1, 'title': 'score2', 'url': 'url_score2'}])
        self.assertEquals(3, result[0][0])
        self.assertEquals(2, result[1][0])
        self.assertEquals(1, result[2][0])

    def test_sort_authors_by_submission_score(self):
        result = ProcessData.sort_authors_by_submission_score([{'submitter': 'user1', 'punctuation': 2,
                                                                'submission_title': 'title1'},
                                                               {'submitter': 'user1', 'punctuation': 3,
                                                                'submission_title': 'title2'},
                                                               {'submitter': 'user2', 'punctuation': 4,
                                                                'submission_title': 'title3'}])
        self.assertEquals((2+3, 'user1'), result[0])
        self.assertEquals((4, 'user2'), result[1])

    def test_sort_authors_by_submissions(self):
        result = ProcessData.sort_authors_by_submissions([{'submitter': 'user1', 'submission_title': 'title1'},
                                                          {'submitter': 'user2', 'submission_title': 'title2'},
                                                          {'submitter': 'user3', 'submission_title': 'title3'},
                                                          {'submitter': 'user2', 'submission_title': 'title4'}])
        self.assertEquals((2, 'user2'), result[0])
        self.assertTrue(result[1] in [(1, 'user1'), (1, 'user3')])
        self.assertTrue(result[2] in [(1, 'user1'), (1, 'user3')])

    def test_sort_authors_by_score(self):
        result = ProcessData.sort_authors_by_score([{'author': 'user1', 'score': 10},
                                                    {'author': 'user2', 'score': 6},
                                                    {'author': 'user3', 'score': 15}])
        self.assertEquals((15, 'user3'), result[0])
        self.assertEquals((10, 'user1'), result[1])
        self.assertEquals((6, 'user2'), result[2])

