import pymongo
import configparser
import argparse
import json
from common import hlog
from use_mongodb import insert_document
from use_mongodb import find_document
from use_mongodb import update_document
from use_mongodb import delete_document

config = configparser.ConfigParser()
config.read('conf/config.ini')
mongodb_connection = config.get('main', 'db_url')
db_name = config.get('main', 'db_name')
collection_name = config.get('main', 'collection_name')

client = pymongo.MongoClient(mongodb_connection)
db = client[db_name]
collection = db[collection_name]


def main():
    parser = argparse.ArgumentParser(prog='mongodb_tool',
                                     description='MongoDB工具',
                                     usage='%(prog)s [-i <data>] [-d <data>] [-s <data>] [-u <data>]')

    parser.add_argument('-i',
                        help='执行插入操作，提供数据（JSON格式）',
                        action='store',
                        dest='insert_data',
                        type=json.loads)

    parser.add_argument('-d',
                        help='执行删除操作，提供查询条件（JSON格式）',
                        action='store',
                        dest='delete_data',
                        type=json.loads)

    parser.add_argument('-s',
                        help='执行查询操作，提供查询条件（JSON格式）',
                        action='store',
                        dest='search_data',
                        type=str,
                        nargs='?',
                        const={},
                        default=None)

    parser.add_argument('-u',
                        help='执行更新操作，提供查询条件和更新数据（JSON格式）',
                        action='store',
                        dest='update_data',
                        type=json.loads)

    args = parser.parse_args()

    hlog.var('args', args)

    if args.insert_data:
        inserted_id = insert_document(collection, args.insert_data)
        hlog.info(f"Inserted data with ID: {inserted_id}")
    elif args.search_data is not None:
        if args.search_data:
            try:
                search_criteria = json.loads(args.search_data)
                found_documents = find_document(collection, search_criteria)
                hlog.info("The following data was queried:")
                for document in found_documents:
                    hlog.info(document)
            except json.JSONDecodeError:
                hlog.error("查询条件必须是JSON格式")
        else:
            found_documents = find_document(collection, {})
            hlog.info("The following data was queried:")
            for document in found_documents:
                hlog.info(document)
    elif args.update_data:
        update_query = {"name": args.update_data["name"]}
        updated_count = update_document(collection, update_query, args.update_data)
        hlog.info(f"Updated {updated_count} data")
    elif args.delete_data:
        deleted_count = delete_document(collection, args.delete_data)
        hlog.info(f"Deleted {deleted_count} data")
    else:
        hlog.error("命令行参数错误，请查看使用说明:")
        parser.print_help()


if __name__ == "__main__":
    main()
