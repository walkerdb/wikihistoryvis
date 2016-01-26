


class Parser(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.revisions = self.get_revision()
        self.article_title = self.get_article_title()

    def get_revision(self):
        page = list(self.input_data["query"]["pages"].values())[0]
        return page["revisions"]

    def get_article_title(self):
        page = list(self.input_data["query"]["pages"].values())[0]
        return page["title"]