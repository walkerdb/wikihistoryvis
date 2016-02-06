import datetime
from operator import itemgetter

from chronyk import Chronyk


class Parser(object):
    def __init__(self, data, username, oldest_date, newest_date):
        self.username = username
        self.oldest_date = oldest_date
        self.newest_date = newest_date
        self.today = datetime.date.today()
        self.total_created_pages = 0

        if not data:
            self.edits = []
            self.edits_by_page = []
            self.total_addition_size = 0
            self.total_removal_size = 0
            self.oldest_edit = ""

        else:
            self.edits = [item for item in data if item['ns'] == 0]
            self.edits_by_page = self.summarize_by_page(self.edits)
            self.total_addition_size = sum([edit['total addition size'] for edit in self.edits_by_page])
            self.total_removal_size = sum([edit['total removal size'] for edit in self.edits_by_page])
            self.oldest_edit = Chronyk(self.edits[-1]["timestamp"])

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

            if edit['sizediff'] < 0:
                results[title]['total removal size'] += edit['sizediff']
            else:
                results[title]['total addition size'] += edit['sizediff']

            results[title]['edit count'] += 1

            if 'new' in edit:
                self.total_created_pages += 1
                results[title]['created page'] = "yes"

        for title, data in results.items():
            results[title]['average edit size'] = int((data['total addition size'] + data['total removal size']) / data['edit count'])
            results[title]['net edit size'] = data['total addition size'] + data['total removal size']

        list_ = []
        for key, value in results.items():
            value["title"] = key
            list_.append(value)

        newlist = sorted(list_, key=itemgetter('edit count'), reverse=True)

        return newlist
