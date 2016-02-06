from operator import itemgetter
import datetime
from chronyk import Chronyk


class Parser(object):
    def __init__(self, edits, oldest_date, newest_date):
        self.oldest_date = oldest_date
        self.newest_date = newest_date
        self.today = datetime.date.today()
        self.timezone = 18000

        self.edits = self.parse_timestamps(edits)
        self.edits_by_page = self.group_by_key("title")
        self.edits_by_user = self.group_by_key("user")

    def parse_timestamps(self, edits):
        parsed_edits = []
        for edit in edits:
            edit["time"] = Chronyk(edit["timestamp"], timezone=self.timezone)
            parsed_edits.append(edit)

        return parsed_edits

    @staticmethod
    def filter_by_date(edits, start_date, end_date):
        filtered_edits = []

        for edit in edits:
            date = Chronyk(edit["timestamp"]).date()
            if date < start_date or date > end_date:
                continue

            filtered_edits.append(edit)

        return filtered_edits

    def get_chronyk_result(self, date):
        return Chronyk(date, timezone=self.timezone)

    def group_by_key(self, key):
        results = {}
        for edit in self.edits:
            self.update_results(results, edit=edit, results_key=edit[key])

        for results_key, summary in results.items():
            self.add_calculated_fields(results, summary, results_key=results_key)

        results_as_list = self.dict_to_list_of_dicts(results, key_text=key)

        return sorted(results_as_list, key=itemgetter('edit count'), reverse=True)

    def update_results(self, results, edit, results_key):
        self.set_defaults_if_new_key(results, results_key)
        self.update_values(edit, results, results_key)

    @staticmethod
    def set_defaults_if_new_key(results, results_key):
        if results_key not in results:
            results[results_key] = {"edit count": 0,
                                    "total addition size": 0,
                                    "total removal size": 0,
                                    "unique items": set()}

    @staticmethod
    def update_values(edit, results, results_key):
        results[results_key]["edit count"] += 1
        results[results_key]["unique items"].add(edit["title"])

        edit_size = edit["newlen"] - edit["oldlen"]
        if edit_size < 0:
            results[results_key]["total removal size"] += edit_size
        else:
            results[results_key]["total addition size"] += edit_size

    @staticmethod
    def add_calculated_fields(results, summary, results_key):
        results[results_key]["net edit size"] = summary["total addition size"] + summary["total removal size"]
        results[results_key]["average edit size"] = int((summary["total addition size"] + summary["total removal size"]) / summary["edit count"])
        results[results_key]["unique items involved"] = len(summary["unique items"])

    @staticmethod
    def dict_to_list_of_dicts(dict_to_tranform, key_text):
        list_ = []
        for key, value in dict_to_tranform.items():
            value[key_text] = key
            list_.append(value)
        return list_
