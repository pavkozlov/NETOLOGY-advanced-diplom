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

LOGIN = ''
PASSWORD = ''


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
    def __init__(self, token=True, **kwargs):
        if token:
            self.vk = self.authorize_in_vk_by_token()
        else:
            self.vk = self.authorize_in_vk_by_login()
        self.find_gender = self.get_own_gender()
        self.city = self.get_own_city()
        self.kwargs = kwargs
        self.write_into_db()

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
        search = self.vk.users.search(count=1000, fields='books,interests,music', **self.kwargs)
        return search['items']

    def write_into_db(self):
        if vkinder_db.all_people.count_documents({}) == 0:
            all_users = self.get_users()
            formated_list = list()
            for people in all_users:
                user = dict()
                user['first_name'] = people['first_name']
                user['last_name'] = people['last_name']
                try:
                    user['books'] = people['books']
                except KeyError:
                    user['books'] = ''
                try:
                    user['music'] = people['music']
                except KeyError:
                    user['music'] = ''
                try:
                    user['interests'] = people['interests']
                except KeyError:
                    user['interests'] = ''
                user['id'] = people['id']
                user['added_time'] = datetime.datetime.now()
                formated_list.append(user)
            vkinder_db.all_people.insert_many(formated_list)

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


if __name__ == '__main__':
    pavel_kozlov = VKinder()
    for i in pavel_kozlov.find_by_books('Кийосаки'):
        print(i)
