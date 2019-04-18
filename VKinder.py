import datetime
import vk_api
from pymongo import MongoClient
import re

TOKEN = '7aea4bcb72aa437b3b5c739a6acf43deeab50869788cd4579d4cacd5aa83ec2f3e000297025eba5ff9e01'


class VKinderDatabase:
    def __init__(self):
        self.client = MongoClient()
        self.vkinder_db = self.client.vkinder_db

    def insert_many_people(self, my_list):
        if self.vkinder_db.all_people.count_documents({}) == 0:
            self.vkinder_db.all_people.insert_many(my_list)

    def find_all_people(self):
        result = self.vkinder_db.all_people.find({})
        return result

    def insert_one(self, my_dict):
        if self.vkinder_db.own_account.count_documents({}) == 0:
            self.vkinder_db.own_account.insert_one(my_dict)

    def find_one(self):
        result = self.vkinder_db.own_account.find({})[0]
        return result

    def insert_many_partners(self, my_list):
        if self.vkinder_db.partners.count_documents({}) == 0:
            self.vkinder_db.partners.insert_many(my_list)

    def find_many_partners(self):
        result = self.vkinder_db.partners.find({})
        return result


class VKinderVK:
    def __init__(self, age_from=18, age_to=18, **kwargs):
        self.vk = self.authorize_by_token()
        self.age_from = age_from
        self.age_to = age_to

        if kwargs.get('sex'):
            self.sex = kwargs['sex']
        else:
            self.sex = self.get_sex()

        if kwargs.get('city'):
            self.city = kwargs['city']
        else:
            self.city = self.get_city()

    def authorize_by_token(self):
        vk_session = vk_api.VkApi(token=TOKEN)
        vk = vk_session.get_api()
        return vk

    def get_city(self):
        city = self.vk.account.getProfileInfo()['city']['id']
        return city

    def get_sex(self):
        sex = self.vk.account.getProfileInfo()['sex']
        return 2 if sex == 1 else 1

    def search_users(self, count=10):
        result = list()
        for i in range(self.age_from, self.age_to + 1):
            search = self.vk.users.search(count=count, fields='books,interests,music', age_from=i, age_to=i,
                                          city=self.city, sex=self.sex)
            result += search['items']
        return result

    def get_groups(self, user_id=None):
        result = self.vk.groups.get(user_id=user_id)['items']
        return result

    def get_my_profile(self):
        result = self.vk.users.get(fields='books,interests,music')[0]
        if len(result['books']) == 0:
            result['books'] = input("Введите ваши предпочтения в книгах: ")
        if len(result['music']) == 0:
            result['music'] = input("Введите ваши предпочтения в музыке: ")
        if len(result['interests']) == 0:
            result['interests'] = input("Введите ваши интересы: ")
        return result


class VKinderData:
    def format_users(self, all_users):
        result = list()
        for people in all_users:
            user = dict()
            user['first_name'] = people['first_name']
            user['last_name'] = people['last_name']

            if people.get('books'):
                user['books'] = people['books']
            else:
                user['books'] = ''
            if people.get('music'):
                user['music'] = people['music']
            else:
                user['music'] = ''
            if people.get('interests'):
                user['interests'] = people['interests']
            else:
                user['interests'] = ''

            try:
                user_groups = VKinderVK.get_groups(self=VKinderVK(), user_id=people['id'])
                user['groups'] = user_groups
            except vk_api.exceptions.ApiError:
                user['groups'] = list()

            user['added_time'] = datetime.datetime.now()
            result.append(user)
        return result

    def format_my_profile(self, my_profile):
        result = {
            'first_name': my_profile['first_name'],
            'last_name': my_profile['last_name'],
            'books': my_profile['books'],
            'music': my_profile['music'],
            'interests': my_profile['interests'],
            'groups': VKinderVK.get_groups(self=VKinderVK()),
            'added_time': datetime.datetime.now()
        }
        return result


class VKinderSearch:
    def find_ideal(self, my_own_profile, all_users_list):
        result = list()

        my_profile = my_own_profile
        all_users = all_users_list

        my_books = re.split('[,.\s]', my_profile['books'])
        my_books = '.*?(' + ')?('.join(my_books) + ').*?'
        my_books = re.compile(my_books, re.IGNORECASE)

        my_music = re.split('[,.\s]', my_profile['music'])
        my_music = '.*?(' + ')?('.join(my_music) + ').*?'
        my_music = re.compile(my_music, re.IGNORECASE)

        my_interests = re.split('[,.\s]', my_profile['interests'])
        my_interests = '.*?(' + ')?('.join(my_interests) + ').*?'
        my_interests = re.compile(my_interests, re.IGNORECASE)

        my_groups = my_profile['groups']

        for i in all_users:
            res = my_books.search(i['books'])
            if res and i not in result:
                result.append(i)
            res = my_music.search(i['music'])
            if res and i not in result:
                result.append(i)
            res = my_interests.search(i['interests'])
            if res and i not in result:
                result.append(i)
            if len(list(set(my_groups).intersection(i['groups']))) > 0 and i not in result:
                result.append(i)

        return result


def run():
    vk = VKinderVK(age_from=18, age_to=200)
    users = vk.search_users(count=100)
    my_account = vk.get_my_profile()

    vk_data = VKinderData()
    users = vk_data.format_users(users)
    my_account = vk_data.format_my_profile(my_account)

    vk_db = VKinderDatabase()
    vk_db.insert_many_people(users)
    vk_db.insert_one(my_account)

    vk_search = VKinderSearch()
    reccomended = vk_search.find_ideal(my_account, users)

    vk_db.insert_many_partners(reccomended)


if __name__ == '__main__':
    run()
