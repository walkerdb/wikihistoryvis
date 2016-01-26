import unittest

from wikihistoryvis import data_parser


class TestDataParser(unittest.TestCase):
    def setUp(self):
        with open(r"C:\Users\dev\PycharmProjects\wikihistoryvis\wikihistoryvis\test_input_data.txt", mode="r") as f:
            self.input_data = eval(f.read())

        self.parser = data_parser.Parser(self.input_data)
        self.revisions = self.input_data["query"]["pages"]["1081"]["revisions"]

    def test_revision_retrieval(self):
        self.assertEquals(self.parser.revisions, self.revisions)

    def test_name_retrieval(self):
        self.assertEquals(self.parser.article_title, "Internet Archive")

