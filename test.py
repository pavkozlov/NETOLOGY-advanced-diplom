import unittest
import VKinder


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.params = {
            'city': 2,
            'sex': 2,
            'age_from': 19,
            'age_to': 21,
            'count': 1
        }

        self.vk_test = VKinder.VKinderVK()
        self.db_test = VKinder.VKinderDatabase()
        self.data_test = VKinder.VKinderData()
        self.vk_test_with_args = VKinder.VKinderVK(city=self.params['city'], sex=self.params['sex'],
                                                   age_to=self.params['age_to'], age_from=self.params['age_from'])
        self.search_test = VKinder.VKinderSearch()

        self.city = self.vk_test.get_city()
        self.sex = self.vk_test.get_sex()
        self.groups_with_arg = self.vk_test.get_groups(1)
        self.groups_without_arg = self.vk_test.get_groups()
        self.user = self.vk_test.search_users(count=self.params['count'])
        self.users = self.vk_test.search_users()
        self.profile = self.vk_test.get_my_profile()

    def tearDown(self):
        pass

    def test_vkinderdatabase(self):
        '''Test: БД возвращает значения в нужном формате'''
        self.assertTrue(type(self.db_test.find_all_people()) == list)
        self.assertTrue(type(self.db_test.find_one()) == dict)
        self.assertTrue(type(self.db_test.find_many_partners()) == list)

    def test_vkindervk(self):
        '''Test: тест класса VKinderVK'''
        '''Test: класс со значениями по умолчанию'''
        self.assertEqual(self.vk_test.age_from, self.vk_test.age_to)
        self.assertEqual(self.vk_test.age_from, 18)
        self.assertEqual(self.vk_test.city, self.city)
        self.assertEqual(self.vk_test.sex, self.sex)

        '''Test: класс с заданными значениями'''
        self.assertEqual(self.vk_test_with_args.age_from, self.params['age_from'])
        self.assertEqual(self.vk_test_with_args.age_to, self.params['age_to'])
        self.assertEqual(self.vk_test_with_args.city, self.params['city'])
        self.assertEqual(self.vk_test_with_args.sex, self.params['sex'])

        '''Test: возвращаемые значения из функций'''
        self.assertTrue(type(self.user) == list)
        self.assertEqual(len(self.user), self.params['count'])
        self.assertTrue(type(self.users) == list)
        self.assertGreater(len(self.users), 1)
        self.assertNotEqual(self.user, self.users)

        self.assertTrue(type(self.groups_with_arg) == list)
        self.assertTrue(type(self.groups_without_arg) == list)
        self.assertNotEqual(self.groups_with_arg, self.groups_without_arg)
        self.assertTrue(type(self.vk_test.get_my_profile()) == dict)

    def test_vkinderdate(self):
        '''Test: тест класса VKinderData'''
        self.assertTrue(type(self.data_test.format_users(self.users)) == list)
        self.assertTrue(type(self.data_test.format_users(self.user)) == list)
        self.assertNotEqual(self.data_test.format_users(self.user), self.data_test.format_users(self.users))
        self.assertTrue(type(self.data_test.format_my_profile(self.profile)) == dict)

    def test_vkindersearch(self):
        '''Test: тест класса VKinderSearch'''
        self.assertTrue(type(self.search_test.find_ideal(self.data_test.format_my_profile(self.profile),
                                                         self.data_test.format_users(self.users))) == list)
