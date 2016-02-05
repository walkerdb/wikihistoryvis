from operator import itemgetter


class Parser(object):
    def __init__(self, edits):
        self.edits = edits
        self.edits_by_page = self.group_edits_by_page(edits)
        self.edits_by_user = self.group_edits_by_user(edits)

    def group_edits_by_page(self, edits):
        results = {}
        for edit in edits:
            title = edit['title']
            if title not in results:
                results[title] = {"edit count": 0,
                                  "total addition size": 0,
                                  "total removal size": 0,
                                  "net edit size": 0,
                                  "average edit size": 0,
                                  "unique users involved": 0,
                                  "unique users": set()}

            results[title]["edit count"] += 1
            edit_size = edit["newlen"] - edit["oldlen"]

            if edit_size < 0:
                results[title]["total removal size"] += edit_size
            else:
                results[title]["total addition size"] += edit_size

            results[title]["unique users"].add(edit["user"])

        for title, summary in results.items():
            results[title]["net edit size"] = summary["total addition size"] + summary["total removal size"]
            results[title]["average edit size"] = int((summary["total addition size"] + summary["total removal size"]) / summary["edit count"])
            results[title]["unique users involved"] = len(summary["unique users"])

        list_ = []
        for key, value in results.items():
            value["title"] = key
            list_.append(value)

        return sorted(list_, key=itemgetter('edit count'), reverse=True)

    def group_edits_by_user(self, edits):
        results = {}
        for edit in edits:
            user = edit['user']
            if user not in results:
                results[user] = {"edit count": 0,
                                  "total addition size": 0,
                                  "total removal size": 0,
                                  "net edit size": 0,
                                  "unique pages involved": 0,
                                  "unique pages": set()}

            results[user]["edit count"] += 1
            edit_size = edit["newlen"] - edit["oldlen"]

            if edit_size < 0:
                results[user]["total removal size"] += edit_size
            else:
                results[user]["total addition size"] += edit_size

            results[user]["unique pages"].add(edit["title"])

        for user, summary in results.items():
            results[user]["net edit size"] = summary["total addition size"] + summary["total removal size"]
            results[user]["average edit size"] = int((summary["total addition size"] + summary["total removal size"]) / summary["edit count"])
            results[user]["unique pages involved"] = len(summary["unique pages"])

        list_ = []
        for key, value in results.items():
            value["user"] = key
            list_.append(value)

        return sorted(list_, key=itemgetter('edit count'), reverse=True)
