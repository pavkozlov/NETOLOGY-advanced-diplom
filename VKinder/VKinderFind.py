import config
import json
import datetime
from bson import json_util



class VKinderFind:
    def __init__(self):
        self.groups = config.SEARCH_PARAMS['groups']
        self.books = config.SEARCH_PARAMS['books']
        self.music = config.SEARCH_PARAMS['music']
        self.interests = config.SEARCH_PARAMS['interests']

        self.total = self.groups + self.books + self.interests + self.music

        self.groups_percent = self.get_percent(self.groups)
        self.books_percent = self.get_percent(self.books)
        self.music_percent = self.get_percent(self.music)
        self.interests_percent = self.get_percent(self.interests)


    def get_percent(self, category):
        result = round(10 * (category / self.total))
        return result

    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def get_json(self, result):
        res = list()
        for i in result:
            d = {
                'id': i['id'],
                'first_name': i['first_name'],
                'last_name': i['last_name'],
                'photos':i['photos']
            }
            res.append(d)
        with open('result.json', 'w', encoding='utf8') as f:
            json.dump(res, f, ensure_ascii=False, indent=2, default=json_util.default)

