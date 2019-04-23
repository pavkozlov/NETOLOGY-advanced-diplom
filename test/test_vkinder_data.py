import unittest
from VKinder import VKinderData
from users import users

TOKEN = input('TOKEN: ')
ID = int(input('ID: '))
class TestVKinderData(unittest.TestCase):
    def setUp(self):
        self.users = users

        self.vk_data = VKinderData.VKinderData(id=ID,
                                                       token=TOKEN,
                                                       all_user=self.users)
        self.vk_data.with_groups = [1234, 4567, 7890]

        self.profile = {'id': 136707281, 'first_name': 'Ангелина', 'last_name': '...', 'is_closed': True,
                        'can_access_closed': True, 'interests': 'Интересы', 'music': 'Музыка', 'books': 'Книги'}

    def tearDown(self):
        pass

    def test_vkinder_data_init(self):
        with self.assertRaises(TypeError):
            vk_data = VKinderData.VKinderData()
            vk_data = VKinderData.VKinderData('1234')
            vk_data = VKinderData.VKinderData(12345)

    def test_vkinder_data_format_users(self):
        formated_list = self.vk_data.format_users()
        self.assertEqual(len(formated_list), len(self.users))
        self.assertTrue(type(formated_list) == list)

    def test_vkinder_data_format_my_profile(self):
        formated_profile = self.vk_data.format_my_profile(self.profile)
        with self.assertRaises(TypeError):
            self.vk_data.format_my_profile()
        self.assertTrue(type(formated_profile) == dict)

if __name__ == '__main__':
    unittest.main()