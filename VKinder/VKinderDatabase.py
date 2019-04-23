from pymongo import MongoClient


class VKinderDatabase:
    def __init__(self):
        self.client = MongoClient()
        self.vkinder_db = self.client.vkinder_db

    def insert_many_people(self, my_list):
        self.vkinder_db.all_people.insert_many(my_list)

    def find_all_people(self):
        result = list(self.vkinder_db.all_people.find({}))
        return result

    def insert_one(self, my_dict):
        self.vkinder_db.own_account.insert_one(my_dict)

    def find_one(self):
        result = self.vkinder_db.own_account.find({})[0]
        return result

    def insert_many_partners(self, my_list):
        self.vkinder_db.partners.insert_many(my_list)

    def find_many_partners(self):
        result = list(self.vkinder_db.partners.find({}))
        return result

    def bases_empty(self):
        if self.vkinder_db.partners.count_documents({}) == 0 and \
                self.vkinder_db.own_account.count_documents({}) == 0 and \
                self.vkinder_db.all_people.count_documents({}) == 0:
            return True
        else:
            return False
