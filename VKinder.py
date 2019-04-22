import datetime
import vk_api
from pymongo import MongoClient
import re

TOKEN = ''
ID = '19541420'


def authorize_by_token():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    return vk


VK = authorize_by_token()


class VKinderDatabase:
    def __init__(self):
        self.client = MongoClient()
        self.vkinder_db = self.client.vkinder_db

    def insert_many_people(self, my_list):
        if self.vkinder_db.all_people.count_documents({}) == 0:
            self.vkinder_db.all_people.insert_many(my_list)

    def find_all_people(self):
        result = list(self.vkinder_db.all_people.find({}))
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
        result = list(self.vkinder_db.partners.find({}))
        return result

    def bases_non_empty(self):
        if self.vkinder_db.partners.count_documents({}) != 0 and \
                self.vkinder_db.own_account.count_documents({}) != 0 and \
                self.vkinder_db.all_people.count_documents({}) != 0:
            return True
        else:
            return False


class VKinderVK:
    def __init__(self, age_from=18, age_to=18, **kwargs):

        self.age_from = age_from
        self.age_to = age_to
        self.kwargs = kwargs
        self.city = ''
        self.sex = ''

    def paste_info(self):
        if self.kwargs.get('sex'):
            self.sex = self.kwargs['sex']
        else:
            self.sex = self.get_sex()

        if self.kwargs.get('city'):
            self.city = self.kwargs['city']
        else:
            self.city = self.get_city()

    def get_city(self):
        city = VK.users.get(user_ids=ID, fields='city')[0]['city']['id']
        return city

    def get_sex(self):
        sex = VK.users.get(user_ids=ID, fields='sex')[0]['sex']
        return 2 if sex == 1 else 1

    def search_users(self, count=1000):
        result = list()
        for i in range(self.age_from, self.age_to + 1):
            search = VK.users.search(count=count, fields='books,interests,music', age_from=i,
                                     age_to=i, city=self.city, sex=self.sex)
            result += search['items']
        return result

    def get_groups(self, user_id=ID):
        result = VK.groups.get(user_id=user_id)['items']
        return result

    def is_member(self, group_id, users):
        result = VK.groups.isMember(group_id=group_id, user_ids=users)
        return result

    def get_my_profile(self):
        result = VK.users.get(user_ids=ID, fields='books,interests,music')[0]
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
        vk = VKinderVK()
        user_ids = [i['id'] for i in all_users]
        user_ids = map(str, user_ids)
        user_ids = ','.join(user_ids)
        my_grops = vk.get_groups()
        with_groups = list()
        for i in my_grops:
            res = vk.is_member(i, user_ids)
            for user in res:
                if user['member'] == 1:
                    with_groups.append(user['user_id'])

        for people in all_users:
            user = dict()
            user['id'] = people['id']
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

            if people['id'] in with_groups:
                user['groups'] = True
            else:
                user['groups'] = False

            user['added_time'] = datetime.datetime.now()
            result.append(user)
        return result

    def format_my_profile(self, my_profile):
        vk = VKinderVK()
        result = {
            'first_name': my_profile['first_name'],
            'last_name': my_profile['last_name'],
            'books': my_profile['books'],
            'music': my_profile['music'],
            'interests': my_profile['interests'],
            'groups': vk.get_groups(),
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

        for i in all_users:
            if i['groups']:
                result.append(i)
            res = my_books.search(i['books'])
            if res and i not in result:
                result.append(i)
            res = my_music.search(i['music'])
            if res and i not in result:
                result.append(i)
            res = my_interests.search(i['interests'])
            if res and i not in result:
                result.append(i)

        return result


def run():
    vk_db = VKinderDatabase()
    vk_search = VKinderSearch()
    vk_vk = VKinderVK(age_from=18, age_to=23)
    vk_vk.paste_info()
    vk_data = VKinderData()

    users = vk_vk.search_users()
    my_account = vk_vk.get_my_profile()

    users = vk_data.format_users(users)
    my_account = vk_data.format_my_profile(my_account)

    vk_db.insert_many_people(users)
    vk_db.insert_one(my_account)

    reccomended = vk_search.find_ideal(my_account, users)

    vk_db.insert_many_partners(reccomended)


if __name__ == '__main__':
    run()
