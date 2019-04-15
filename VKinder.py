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
            search = self.vk.users.search(count=1000, fields='books,interests,music', age_from=i, age_to=i, **self.kwargs)
            result.append(search['items'])
        return result

    def write_into_db(self):
        if vkinder_db.all_people.count_documents({}) == 0:
            all_users = self.get_users()
            formated_list = list()
            pattern = ',\s?|\.\s?,?'
            pattern = re.compile(pattern)

            for peoples in all_users:
                for people in peoples:
                    user = dict()

                    user['first_name'] = people['first_name']
                    user['last_name'] = people['last_name']

                    try:
                        user_books = people['books']
                        if len(user_books) > 0:
                            user['books'] = re.split(pattern, user_books)
                        else:
                            raise KeyError
                    except KeyError:
                        user['books'] = list()

                    try:
                        user_music = people['music']
                        if len(user_music) > 0:
                            user['music'] = re.split(pattern, user_music)
                        else:
                            raise KeyError
                    except KeyError:
                        user['music'] = list()

                    try:
                        user_interests = people['interests']
                        if len(user_interests) > 0:
                            user['interests'] = re.split(pattern, user_interests)
                        else:
                            raise KeyError
                    except KeyError:
                        user['interests'] = list()

                    try:
                        user_groups = self.find_groups(people['id'])
                        user['groups'] = user_groups
                    except vk_api.exceptions.ApiError:
                        user['groups'] = list()

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
            pattern = '[.,;]'
            pattern = re.compile(pattern)
            my_books = result[0]['books'].split()

            if len(my_books) == 0:
                my_books = input("Введите ваши предпочтения в книгах: ")
                my_books = re.split(pattern, my_books)

            my_music = result[0]['music']
            if len(my_music) == 0:
                my_music = input("Введите ваши предпочтения в музыке: ")
                my_music = re.split(pattern, my_music)

            my_interests = result[0]['interests']
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

    def find_ideal(self):
        ideal_for_me = list()
        me = vkinder_db.own_account.find({})
        partners = vkinder_db.all_people.find({})

        my_books = me[0]['books']
        re_books = "(" + ")|(".join(my_books) + ")"
        re_books = re.compile(re_books)

        my_music = me[0]['music']
        re_music = "(" + ")|(".join(my_music) + ")"
        re_music = re.compile(re_music)

        my_interests = me[0]['interests']
        re_interests = "(" + ")|(".join(my_interests) + ")"
        re_interests = re.compile(re_interests)

        my_groups = me[0]['groups']

        for i in partners:

            both_in_group = list(set(i['groups']).intersection(my_groups))
            if len(both_in_group) > 0 and i not in ideal_for_me:
                ideal_for_me.append(i)

            same_books = list(filter(re_books.search, i['books']))
            if len(same_books) > 0 and i not in ideal_for_me:
                ideal_for_me.append(i)

            same_music = list(filter(re_music.search, i['music']))
            if len(same_music) > 0 and i not in ideal_for_me:
                ideal_for_me.append(i)

            same_interests = list(filter(re_interests.search, i['interests']))
            if len(same_interests) > 0 and i not in ideal_for_me:
                ideal_for_me.append(i)

            del i

        vkinder_db.ideal_partner.insert_many(ideal_for_me)


if __name__ == '__main__':
    pavel_kozlov = VKinder(token=False, age_from=18, age_to=20)
    pavel_kozlov.find_ideal()
