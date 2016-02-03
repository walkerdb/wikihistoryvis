import unittest

from wikihistoryvis import article_revision_parser


class TestDataParser(unittest.TestCase):
    def setUp(self):
        with open(r"C:\Users\dev\PycharmProjects\wikihistoryvis\wikihistoryvis\test_input_data.txt", mode="r") as f:
            self.input_data = eval(f.read())
        self.test_revisions = self.input_data["query"]["pages"]["1081"]["revisions"]
        self.test_revisions.reverse()

        self.parser = article_revision_parser.Parser(self.input_data)

    def test_revision_retrieval(self):
        self.assertEquals(self.parser.revisions, self.test_revisions)

    def test_name_retrieval(self):
        self.assertEquals(self.parser.article_title, "Internet Archive")

    def test_add_change_sizes(self):
        test_data = [{"size": 1}, {"size": 3}, {"size": 6}]
        intended_results = [{"change_size": 1, "size": 1}, {"change_size": 2, "size": 3}, {"change_size": 3, "size": 6}]
        self.assertEquals(self.parser.add_edit_sizes(test_data), intended_results)
