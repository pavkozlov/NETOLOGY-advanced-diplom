import vk_api
from urllib.parse import urlencode
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


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


access_token = get_access_token('login', 'password')


class VKinder:
    def __init__(self, **kwargs):
        self.vk = self.authorize_in_vk()
        self.find_gender = self.get_own_gender()
        self.city = self.get_own_city()
        self.kwargs = kwargs

    def authorize_in_vk(self):
        vk_session = vk_api.VkApi(token=access_token)
        vk = vk_session.get_api()
        return vk

    def get_users(self):
        if self.kwargs.get('sex') == None:
            self.kwargs['sex'] = self.find_gender
        if self.kwargs.get('city') == None:
            self.kwargs['city'] = self.city
        search = self.vk.users.search(count=1000, fields='books,interests,age', **self.kwargs)
        return search['items']

    def get_own_city(self):
        city = self.vk.account.getProfileInfo()['city']['id']
        return city

    def get_own_gender(self):
        gender = self.vk.account.getProfileInfo()['sex']
        if gender == 1:
            return 2
        else:
            return 1

    def get_users_with_books_and_interests(self):
        result = list()
        user_list = self.get_users()
        for user in user_list:
            if user.get('books') and user.get('interests'):
                result.append(user)
        return result


if __name__ == '__main__':
    pavel_kozlov = VKinder(sex=2)
    print(pavel_kozlov.get_users_with_books_and_interests())
