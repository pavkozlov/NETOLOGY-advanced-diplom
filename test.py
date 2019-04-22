import unittest
import VKinder


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.db_test = VKinder.VKinderDatabase()

        self.vk_test = VKinder.VKinderVK()
        self.vk_users = self.vk_test.search_users(count=5)
        self.my_profile = self.vk_test.get_my_profile()

        self.vk_data = VKinder.VKinderData()
        self.my_profile = self.vk_data.format_my_profile(self.my_profile)
        self.all_users = self.vk_data.format_users(self.vk_users)

        self.vk_search = VKinder.VKinderSearch()

    def tearDown(self):
        pass

    def test_vkinderdatabase(self):
        self.assertTrue(type(self.db_test.bases_non_empty()) == bool)
        if self.db_test.bases_non_empty():
            self.assertTrue(type(self.db_test.find_all_people()) == list)
            self.assertTrue(type(self.db_test.find_one()) == dict)
            self.assertTrue(type(self.db_test.find_many_partners()) == list)

    def test_vkindervk(self):
        self.assertTrue(type(self.vk_test.get_city()) == int)
        self.assertTrue(type(self.vk_test.get_sex()) == int)
        self.assertTrue(type(self.vk_users) == list)
        self.assertTrue(type(self.vk_test.get_groups()) == list)
        self.assertTrue(type(self.my_profile) == dict)
        self.assertTrue(type(self.vk_test.is_member('1', '1,2,3,4,5')) == list)

    #
    def test_vkinderdate(self):
        self.assertTrue(type(self.all_users) == list)
        self.assertTrue(type(self.my_profile) == dict)

    def test_vkindersearch(self):
        search = self.vk_search.find_ideal(self.my_profile, self.all_users)
        self.assertTrue(type(search) == list)
