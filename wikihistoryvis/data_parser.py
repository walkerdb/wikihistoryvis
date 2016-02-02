import datetime
from operator import itemgetter


class Parser(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.revisions = self.create_revisions_list()
        self.article_title = self.get_article_title()
        self.user_summaries = self.create_user_summaries()

    def create_revisions_list(self):
        revisions = self.get_revision()
        revisions.reverse()
        revisions = self.add_edit_sizes(revisions)
        revisions = self.add_formatted_dates(revisions)

        return revisions

    def get_revision(self):
        page = list(self.input_data["query"]["pages"].values())[0]
        return page["revisions"]

    def get_article_title(self):
        page = list(self.input_data["query"]["pages"].values())[0]
        return page["title"]

    def create_user_summaries(self):
        results = {}
        for revision in self.revisions:
            user = revision["user"]
            time = datetime.datetime.strptime(revision["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            if user not in results:
                results[user] = {"number of revisions": 0, "total size of changes": 0, "times of changes": []}

            results[user]["number of revisions"] += 1
            results[user]["total size of changes"] += abs(int(revision.get("change_size", 0)))
            results[user]["times of changes"].append(time)

        for user, data in results.items():
            results[user]["average edit size"] = int(data["total size of changes"] / data["number of revisions"])

        list_ = []
        for key, value in results.items():
            value["user"] = key
            list_.append(value)

        newlist = sorted(list_, key=itemgetter('number of revisions'), reverse=True)

        return newlist

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

    def add_formatted_dates(self, revisions):
        new_revisions = []

        for revision in revisions:
            revision["formatted date"] = revision["timestamp"].replace("T", " ").strip("Z")
            new_revisions.append(revision)

        return new_revisions