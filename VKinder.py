import datetime
import vk_api
from urllib.parse import urlencode
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pymongo import MongoClient

client = MongoClient()
vkinder_db = client.vkinder_db

LOGIN = 'login'
PASSWORD = 'password'


def get_access_token(my_login, my_password):
    app_id = 6854739
    auth_url = 'https://oauth.vk.com/authorize'
    auth_data = {
        'client_id': app_id,
        'display': 'page',
        'scope': 'status, friends',
        'response_type': 'token',
        'v': '5.95',
        'redirect_uri': ''
    }
    url = '?'.join((auth_url, urlencode(auth_data)))

    browser = webdriver.Firefox()
    browser.get(url)
    login = browser.find_element_by_name('email')
    password = browser.find_element_by_name('pass')
    login.send_keys(my_login)
    password.send_keys(my_password)
    password.send_keys(Keys.ENTER)
    time.sleep(1)
    url = browser.current_url
    browser.quit()
    pattern = 'access_token=(.*)&expires_in'
    re.compile(pattern)
    res = re.search(pattern, url).group(1)
    return res


class VKinder:
    def __init__(self, age_from, age_to, token=True, **kwargs):
        print('Начали: ', datetime.datetime.now())
        self.age_from = age_from
        self.age_to = age_to + 1
        if token:
            self.vk = self.authorize_in_vk_by_token()
        else:
            self.vk = self.authorize_in_vk_by_login()
        self.find_gender = self.get_own_gender()
        self.city = self.get_own_city()
        self.kwargs = kwargs
        self.write_into_db()
        self.get_own_books_and_interests()

    def authorize_in_vk_by_token(self):
        access_token = get_access_token(LOGIN, PASSWORD)
        vk_session = vk_api.VkApi(token=access_token)
        vk = vk_session.get_api()
        return vk

    def authorize_in_vk_by_login(self):
        vk_session = vk_api.VkApi(login=LOGIN, password=PASSWORD)
        vk_session.auth()
        vk = vk_session.get_api()
        return vk

    def get_users(self):
        if self.kwargs.get('sex') == None:
            self.kwargs['sex'] = self.find_gender
        if self.kwargs.get('city') == None:
            self.kwargs['city'] = self.city
        result = list()
        for i in range(self.age_from, self.age_to):
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
            print('Закончили: ', datetime.datetime.now())

    def find_by_books(self, name):
        escaped_name = re.escape(name)
        pattern = re.compile(r'(.*?{}.*?)'.format(escaped_name), re.IGNORECASE)
        res = vkinder_db.all_people.find({'books': pattern})
        result = list()
        for item in res:
            result.append([item['id'], item['first_name'], item['last_name'], item['books']])
        return result

    def get_own_city(self):
        city = self.vk.account.getProfileInfo()['city']['id']
        return city

    def get_own_gender(self):
        gender = self.vk.account.getProfileInfo()['sex']
        if gender == 1:
            return 2
        else:
            return 1

    def find_groups(self, user_id=None):
        res = self.vk.groups.get(user_id=user_id)['items']
        return res

    def get_own_books_and_interests(self):

        if vkinder_db.own_account.count_documents({}) == 0:
            result = self.vk.users.get(fields='books,interests,music')
            pattern = re.escape(', ')
            pattern = re.compile(pattern)
            try:
                my_books = re.split(pattern, result[0]['books'])
            except KeyError:
                my_books = input("Введите ваши предпочтения в книгах: ")
                my_books = re.split(pattern, my_books)
            try:
                my_music = re.split(pattern, result[0]['music'])
            except KeyError:
                my_music = input("Введите ваши предпочтения в музыке: ")
                my_music = re.split(pattern, my_music)
            try:
                my_interests = re.split(pattern, result[0]['interests'])
            except KeyError:
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
