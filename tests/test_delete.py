import configparser
import unittest
import pymongo
from pymongo import MongoClient
from method.mongodb_base import delete_document
from method.mongodb_base import insert_document


config = configparser.ConfigParser()
config.read('../conf/config.ini')
mongodb_connection = config.get('main', 'db_url')
db_name = config.get('main', 'db_name')
collection_name = config.get('main', 'collection_name')

client = pymongo.MongoClient(mongodb_connection)
db = client[db_name]
collection = db[collection_name]


class TestDeleteDocument(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient(mongodb_connection)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        self.collection.delete_many({})

        initial_data = [{"name": "Bob", "age": 25}]
        for data in initial_data:
            insert_document(self.collection, data)

    def tearDown(self):
        self.client.close()

    def test_delete_document(self):
        query = {"name": "Bob"}
        deleted_count = delete_document(self.collection, query)
        self.assertEqual(deleted_count, 1)


if __name__ == '__main__':
    unittest.main()
