import configparser
import unittest

import pymongo
from pymongo import MongoClient

from method.use_mongodb import find_document
from method.use_mongodb import insert_document

config = configparser.ConfigParser()
config.read('../conf/config.ini')
mongodb_connection = config.get('main', 'db_url')
db_name = config.get('main', 'db_name')
collection_name = config.get('main', 'collection_name')

client = pymongo.MongoClient(mongodb_connection)
db = client[db_name]
collection = db[collection_name]


class TestFindDocument(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient(mongodb_connection)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        self.collection.delete_many({})

        initial_data = [{"name": "woman", "age": 30}]
        for data in initial_data:
            insert_document(self.collection, data)

    def tearDown(self):
        self.client.close()

    def test_find_document(self):
        query = {"name": "woman"}
        results = find_document(self.collection, query)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "woman")


if __name__ == '__main__':
    unittest.main()
