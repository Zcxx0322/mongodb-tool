import configparser
import unittest

import pymongo
from pymongo import MongoClient

from method.mongodb_base import insert_document
from method.mongodb_base import update_document

config = configparser.ConfigParser()
config.read('../conf/config.ini')
mongodb_connection = config.get('main', 'db_url')
db_name = config.get('main', 'db_name')
collection_name = config.get('main', 'collection_name')

client = pymongo.MongoClient(mongodb_connection)
db = client[db_name]
collection = db[collection_name]


class TestUpdateDocument(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient(mongodb_connection)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        initial_data = [{"name": "Alice", "age": 25}]
        for data in initial_data:
            insert_document(self.collection, data)

    def tearDown(self):
        self.client.close()

    def test_update_document(self):
        query = {"name": "Alice"}
        new_data = {"age": 31}
        modified_count = update_document(self.collection, query, new_data)
        self.assertEqual(modified_count, 1)

        self.collection.delete_many({})


if __name__ == '__main__':
    unittest.main()
