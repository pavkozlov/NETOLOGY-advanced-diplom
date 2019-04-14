import datetime
import vk_api
from pymongo import MongoClient
import get_token_from_login
import re

client = MongoClient()
vkinder_db = client.vkinder_db

# INPUT YOUR TOKEN HERE!!!
TOKEN = get_token_from_login.get_access_token(get_token_from_login.LOGIN, get_token_from_login.PASSWORD)


class VKinder:
    def __init__(self, age_from, age_to, **kwargs):
        self.age_from = age_from
        self.age_to = age_to
        self.kwargs = kwargs

        self.vk = self.authorize_in_vk_by_token()

        self.find_gender = self.get_own_gender()
        self.city = self.get_own_city()

        self.write_into_db()
        self.get_own_books_and_interests()

    def authorize_in_vk_by_token(self):
        access_token = TOKEN
        vk_session = vk_api.VkApi(token=access_token)
        vk = vk_session.get_api()
        return vk

    def get_users(self):
        if self.kwargs.get('sex') == None:
            self.kwargs['sex'] = self.find_gender

        if self.kwargs.get('city') == None:
            self.kwargs['city'] = self.city

        result = list()
        for i in range(self.age_from, self.age_to + 1):
            search = self.vk.users.search(count=10, fields='books,interests,music', age_from=i, age_to=i, **self.kwargs)
            result.append(search['items'])
        return result

    def write_into_db(self):
        if vkinder_db.all_people.count_documents({}) == 0:
            all_users = self.get_users()
            formated_list = list()
            pattern = re.escape(', ')
            pattern = re.compile(pattern)

            for peoples in all_users:
                for people in peoples:
                    user = dict()

                    user['first_name'] = people['first_name']
                    user['last_name'] = people['last_name']

                    try:
                        user['books'] = re.split(pattern, people['books'])
                    except KeyError:
                        user['books'] = list()

                    try:
                        user['music'] = re.split(pattern, people['music'])
                    except KeyError:
                        user['music'] = list()

                    try:
                        user['interests'] = re.split(pattern, people['interests'])
                    except KeyError:
                        user['interests'] = list()

                    user['id'] = people['id']
                    user['added_time'] = datetime.datetime.now()

                    try:
                        user_groups = self.find_groups(people['id'])
                        user['groups'] = user_groups
                    except vk_api.exceptions.ApiError:
                        user['groups'] = ''

                    formated_list.append(user)

            vkinder_db.all_people.insert_many(formated_list)

    def get_own_city(self):
        city = self.vk.account.getProfileInfo()['city']['id']
        return city

    def get_own_gender(self):
        gender = self.vk.account.getProfileInfo()['sex']
        if gender == 1:
            return 2
        elif gender == 2:
            return 1

    def find_groups(self, user_id=None):
        res = self.vk.groups.get(user_id=user_id)['items']
        return res

    def get_own_books_and_interests(self):

        if vkinder_db.own_account.count_documents({}) == 0:
            result = self.vk.users.get(fields='books,interests,music')
            pattern = re.escape(', ')
            pattern = re.compile(pattern)
            my_books = re.split(pattern, result[0]['books'])

            if len(my_books) == 0:
                my_books = input("Введите ваши предпочтения в книгах: ")
                my_books = re.split(pattern, my_books)

            my_music = re.split(pattern, result[0]['music'])
            if len(my_music) == 0:
                my_music = input("Введите ваши предпочтения в музыке: ")
                my_music = re.split(pattern, my_music)

            my_interests = re.split(pattern, result[0]['interests'])
            if len(my_interests) == 0:
                my_interests = input("Введите ваши интересы: ")
                my_interests = re.split(pattern, my_interests)

            vkinder_db.own_account.insert_one({
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name'],
                'books': my_books,
                'music': my_music,
                'interests': my_interests,
                'id': result[0]['id'],
                'added_time': datetime.datetime.now(),
                'groups': self.find_groups()
            })


if __name__ == '__main__':
    pavel_kozlov = VKinder(token=False, age_from=19, age_to=20)
