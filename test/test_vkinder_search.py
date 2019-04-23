import unittest
from VKinder import VKinderSearch
from users import users


class TestVkinderSearch(unittest.TestCase):
    def setUp(self):
        self.users = users
        self.my_profile = self.users[0]
        self.all_users = self.users
        self.vk_search = VKinderSearch.VKinderSearch(self.my_profile, self.all_users)

    def tearDown(self) -> None:
        pass

    def test_find(self):
        self.assertTrue(type(self.vk_search.find_with_books()) == list)
        self.assertTrue(type(self.vk_search.find_with_music()) == list)
        self.assertTrue(type(self.vk_search.find_with_interests()) == list)
        self.assertTrue(type(self.vk_search.find_with_groups()) == list)

if __name__ == '__main__':
    unittest.main()