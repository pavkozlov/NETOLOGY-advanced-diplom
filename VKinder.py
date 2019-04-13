import vk_api


class VKinder:
    def __init__(self, login, password, **kwargs):
        self.login = login
        self.password = password
        self.vk = self.authorize_in_vk(self.login, self.password)
        self.find_gender = self.get_own_gender()
        self.city = self.get_own_city()
        self.kwargs = kwargs

    def authorize_in_vk(self, login, password):
        vk_session = vk_api.VkApi(login, password)
        vk_session.auth()
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


pavel_kozlov = VKinder('+79660684435', '', sex=1)
print(pavel_kozlov.get_users_with_books_and_interests())
