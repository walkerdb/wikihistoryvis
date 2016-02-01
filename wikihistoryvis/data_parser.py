
class Parser(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.revisions = self.get_revision()
        self.revisions.reverse()
        self.revisions = self.add_edit_sizes(self.revisions)
        self.article_title = self.get_article_title()

    def get_revision(self):
        page = list(self.input_data["query"]["pages"].values())[0]
        return page["revisions"]

    def get_article_title(self):
        page = list(self.input_data["query"]["pages"].values())[0]
        return page["title"]

    def add_edit_sizes(self, revisions):
        new_revisions = []

        first_revision = revisions[0]
        first_revision["change_size"] = first_revision["size"]

        new_revisions.append(first_revision)

        last_size = revisions[0]["size"]

        for revision in revisions[1:]:
            revision["change_size"] = revision["size"] - last_size
            new_revisions.append(revision)
            last_size = revision["size"]

        return new_revisions