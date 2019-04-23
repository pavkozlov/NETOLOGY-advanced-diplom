import unittest
from VKinder import VKinderDatabase
from pymongo import MongoClient
from users import users


class TestVKinderDataBase(unittest.TestCase):
    def setUp(self):
        self.users = users
        self.vk_db = VKinderDatabase.VKinderDatabase()
        self.client = MongoClient()
        self.vkinder_db = self.client.vkinder_db
        self.bases_empty = self.vk_db.bases_empty()

    def tearDown(self) -> None:
        pass

    def test_returned_values(self):
        if self.bases_empty:
            with self.assertRaises(IndexError):
                self.vk_db.find_many_partners()
                self.vk_db.find_one()
                self.vk_db.find_all_people()
            self.vk_db.insert_many_people(self.users)
            self.vk_db.insert_many_partners(self.users)
            self.vk_db.insert_one(self.users[0])
            self.assertTrue(not self.vk_db.bases_empty())
            self.vk_db.client.drop_database('vkinder_db')
            self.assertTrue(self.vk_db.bases_empty())

        else:
            partners = self.vk_db.find_many_partners()
            profile = self.vk_db.find_one()
            users = self.vk_db.find_all_people()
            self.assertTrue(type(partners) == list)
            self.assertTrue(type(users) == list)
            self.assertTrue(type(profile) == dict)

if __name__ == '__main__':
    unittest.main()