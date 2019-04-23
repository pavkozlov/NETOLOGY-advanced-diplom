import vk_api


class VKinderVK:
    def __init__(self, id, token, age_from=18, age_to=18, **kwargs):
        self.token = token
        self.id = id
        self.sex = None
        self.city = None
        self.VK = None
        self.age_from = age_from
        self.age_to = age_to
        self.kwargs = kwargs

    def authorize_by_token(self):
        vk_session = vk_api.VkApi(token=self.token)
        vk = vk_session.get_api()
        self.VK = vk

    def get_city_and_sex(self):
        if self.kwargs.get('sex'):
            self.sex = self.kwargs['sex']
        else:
            self.sex = self.get_sex()

        if self.kwargs.get('city'):
            self.city = self.kwargs['city']
        else:
            self.city = self.get_city()

    def get_city(self):
        city = self.VK.users.get(user_ids=self.id, fields='city')[0]['city']['id']
        return city

    def get_sex(self):
        sex = self.VK.users.get(user_ids=self.id, fields='sex')[0]['sex']
        return 2 if sex == 1 else 1

    def search_users(self, count=1000):
        result = list()
        for year in range(self.age_from, self.age_to + 1):
            search = self.VK.users.search(count=count, fields='books,interests,music',
                                          age_from=year, age_to=year, city=self.city, sex=self.sex)
            result += search['items']
        return result

    def get_groups(self):
        result = self.VK.groups.get(user_id=self.id)['items']
        return result

    def is_member(self, group_id, users):
        try:
            result = self.VK.groups.isMember(group_id=group_id, user_ids=users)
            return result
        except vk_api.exceptions.ApiError:
            result = list()
            return result

    def get_my_profile(self):
        result = self.VK.users.get(user_ids=self.id, fields='books,interests,music')[0]
        if len(result['books']) == 0:
            result['books'] = input("Введите ваши предпочтения в книгах: ")
        if len(result['music']) == 0:
            result['music'] = input("Введите ваши предпочтения в музыке: ")
        if len(result['interests']) == 0:
            result['interests'] = input("Введите ваши интересы: ")
        return result
