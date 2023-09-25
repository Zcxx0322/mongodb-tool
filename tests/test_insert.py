import configparser
import unittest
import pymongo
from pymongo import MongoClient
from method.use_mongodb import insert_document

config = configparser.ConfigParser()
config.read('../conf/config.ini')
mongodb_connection = config.get('main', 'db_url')
db_name = config.get('main', 'db_name')
collection_name = config.get('main', 'collection_name')

client = pymongo.MongoClient(mongodb_connection)
db = client[db_name]
collection = db[collection_name]


class TestInsertDocument(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient(mongodb_connection)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        self.collection.delete_many({})

    def tearDown(self):
        self.client.close()

    def test_insert_document(self):
        new_data = {"name": "man", "age": 28}
        inserted_id = insert_document(self.collection, new_data)
        self.assertIsNotNone(inserted_id)


if __name__ == '__main__':
    unittest.main()
