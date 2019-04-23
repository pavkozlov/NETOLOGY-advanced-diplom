import datetime
from VKinder.VKinderVkontakte import VKinderVK


class VKinderData:
    def __init__(self, token, id, all_user):
        self.id = id
        self.token = token
        self.vk = VKinderVK(token=self.token, id=self.id)
        self.vk.authorize_by_token()
        self.all_users = all_user
        self.with_groups = None

    def users_with_groups(self):
        user_ids = [i['id'] for i in self.all_users]
        user_ids = map(str, user_ids)
        user_ids = ','.join(user_ids)

        my_groups = self.vk.get_groups()
        if len(my_groups) > 0:
            with_groups = list()
            for i in my_groups:
                res = self.vk.is_member(i, user_ids)
                for user in res:
                    if user['member'] == 1:
                        with_groups.append(user['user_id'])
            self.with_groups = with_groups
            return with_groups
        else:
            result = list()
            return result

    def format_users(self):
        result = list()

        for people in self.all_users:
            user = dict()
            user['id'] = people['id']
            user['first_name'] = people['first_name']
            user['last_name'] = people['last_name']
            user['books'] = people['books'] if people.get('books') else ''
            user['music'] = people['music'] if people.get('music') else ''
            user['interests'] = people['interests'] if people.get('interests') else ''

            if people['id'] in self.with_groups:
                user['groups'] = True
            else:
                user['groups'] = False

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
            'groups': self.vk.get_groups(),
            'added_time': datetime.datetime.now()
        }
        return result
