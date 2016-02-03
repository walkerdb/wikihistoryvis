from operator import itemgetter


class Parser(object):
    def __init__(self, data, username):
        if not data:
            self.edits = []
            self.edits_by_page = []
            self.total_addition_size = 0
            self.total_removal_size = 0
        else:
            self.edits = [item for item in data if item['ns'] == 0]
            self.edits_by_page = self.summarize_by_page(self.edits)
            self.total_addition_size = sum([edit['total addition size'] for edit in self.edits_by_page])
            self.total_removal_size = sum([edit['total removal size'] for edit in self.edits_by_page])

        self.username = username.lower()

    def summarize_by_page(self, edits):
        results = {}
        for edit in edits:
            title = edit['title']

            # set up default values
            if title not in results:
                results[title] = {'total addition size': 0,
                                  'total removal size': 0,
                                  'net edit size': 0,
                                  'average edit size': 0,
                                  'edit count': 0,
                                  'created page': "-"}

            if edit['size'] < 0:
                results[title]['total removal size'] += edit['size']
            else:
                results[title]['total addition size'] += edit['size']

            results[title]['edit count'] += 1

            if 'new' in edit:
                results[title]['created page'] = "yes"

        for title, data in results.items():
            results[title]['average edit size'] = int((data['total addition size'] + abs(data['total removal size'])) / data['edit count'])
            results[title]['net edit size'] = data['total addition size'] + data['total removal size']

        list_ = []
        for key, value in results.items():
            value["title"] = key
            list_.append(value)

        newlist = sorted(list_, key=itemgetter('edit count'), reverse=True)

        return newlist
