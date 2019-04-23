import re


class VKinderSearch:
    def __init__(self, my_own_profile, all_users_list):
        self.my_profile = my_own_profile
        self.all_users = all_users_list

    def find_with_books(self):
        result = list()
        my_books_regex = re.split('[,.\s]', self.my_profile['books'])
        my_books_regex = '.*?(' + ')?('.join(my_books_regex) + ').*?'
        my_books_regex = re.compile(my_books_regex, re.IGNORECASE)

        for user in self.all_users:
            res = my_books_regex.search(user['books'])
            if res:
                result.append(user)
        return result

    def find_with_music(self):
        result = list()
        my_music_regex = re.split('[,.\s]', self.my_profile['music'])
        my_music_regex = '.*?(' + ')?('.join(my_music_regex) + ').*?'
        my_music_regex = re.compile(my_music_regex, re.IGNORECASE)

        for user in self.all_users:
            res = my_music_regex.search(user['music'])
            if res:
                result.append(user)
        return result

    def find_with_interests(self):
        result = list()
        my_interests_regex = re.split('[,.\s]', self.my_profile['interests'])
        my_interests_regex = '.*?(' + ')?('.join(my_interests_regex) + ').*?'
        my_interests_regex = re.compile(my_interests_regex, re.IGNORECASE)

        for user in self.all_users:
            res = my_interests_regex.search(user['interests'])
            if res:
                result.append(user)
        return result

    def find_with_groups(self):
        result = list()

        for user in self.all_users:
            if user['groups']:
                result.append(user)
        return result
