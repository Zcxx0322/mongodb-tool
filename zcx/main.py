import argparse
import configparser
import json
import os
import sys

import pymongo
import pymongo.errors
from happy_python import HappyLog

from .method.file_create import create_config_if_not_exists
from .method.mongodb_base import delete_document
from .method.mongodb_base import find_document
from .method.mongodb_base import insert_document
from .method.mongodb_base import update_document
from .method.mongodb_dump import dump_data_to_file
from .method.mongodb_import import import_data_from_file

user_home = os.path.expanduser("~")

DEFAULT_CONFIG_PATH = os.path.join(user_home, ".zcx", "config.ini")
DEFAULT_LOG_CONFIG_PATH = os.path.join(user_home, ".zcx", "log.ini")


class _ChineseArgumentParser(argparse.ArgumentParser):
    """将 argparse 自动生成的英文节标题和错误提示替换为中文。"""

    def format_help(self):
        text = super().format_help()
        text = text.replace('usage:', '用法:')
        text = text.replace('\noptions:\n', '\n选项:\n')
        text = text.replace('\noptional arguments:\n', '\n选项:\n')
        return text

    def format_usage(self):
        return super().format_usage().replace('usage:', '用法:')

    def error(self, message):
        self.print_usage(sys.stderr)
        print(f'{self.prog}: 错误: {message}', file=sys.stderr)
        sys.exit(2)


def main():
    create_config_if_not_exists()

    parser = _ChineseArgumentParser(prog='zcx',
                                    description='MongoDB 命令行管理工具',
                                    usage='%(prog)s [-c <配置文件>] [-l <日志配置文件>] [-i <数据>] [-d <数据>]'
                                          ' [-s [数据]] [-u <数据>] [--dump <文件名>] [--import <文件名>]',
                                    add_help=False)

    parser.add_argument('-h', '--help',
                        action='help',
                        help='显示此帮助信息并退出')

    parser.add_argument('-c',
                        metavar='配置文件',
                        help='配置文件路径，默认为 ~/.zcx/config.ini',
                        default=None)

    parser.add_argument('-l',
                        metavar='日志配置文件',
                        help='日志配置文件路径，默认为 ~/.zcx/log.ini',
                        default=None)

    parser.add_argument('-i',
                        metavar='数据',
                        help='执行插入操作，提供数据（JSON 格式）',
                        action='store',
                        dest='insert_data',
                        type=json.loads)

    parser.add_argument('-d',
                        metavar='条件',
                        help='执行删除操作，提供查询条件（JSON 格式）',
                        action='store',
                        dest='delete_data',
                        type=json.loads)

    parser.add_argument('-s',
                        metavar='条件',
                        help='执行查询操作，提供查询条件（JSON 格式）',
                        action='store',
                        dest='search_data',
                        type=str,
                        nargs='?',
                        const={},
                        default=None)

    parser.add_argument('-u',
                        metavar='数据',
                        help='执行更新操作，提供查询条件和更新数据（JSON 格式）',
                        action='store',
                        dest='update_data',
                        type=json.loads)

    parser.add_argument('--dump',
                        metavar='文件名',
                        help='导出数据到指定文件（JSON 格式）',
                        action='store',
                        dest='dump_file',
                        type=str)

    parser.add_argument('--import',
                        metavar='文件名',
                        help='从指定文件导入数据（JSON 格式）',
                        action='store',
                        dest='import_file',
                        type=str)

    args = parser.parse_args()

    config_file_path = args.c or DEFAULT_CONFIG_PATH

    # ---------- 读取配置文件 ----------
    config = configparser.ConfigParser()

    try:
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"配置文件不存在: '{config_file_path}'")
        config.read(config_file_path, encoding='utf-8')
        mongodb_connection = config.get('main', 'db_url')
        db_name = config.get('main', 'db_name')
        collection_name = config.get('main', 'collection_name')
    except FileNotFoundError as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(1)
    except configparser.NoSectionError as e:
        print(f"[错误] 配置文件缺少必要的节: {e}", file=sys.stderr)
        sys.exit(1)
    except configparser.NoOptionError as e:
        print(f"[错误] 配置文件缺少必要的选项: {e}", file=sys.stderr)
        sys.exit(1)
    except configparser.Error as e:
        print(f"[错误] 配置文件解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    # ---------- 初始化日志 ----------
    log_config_file_path = args.l or DEFAULT_LOG_CONFIG_PATH
    log_ini = log_config_file_path if os.path.exists(log_config_file_path) else ''
    hlog = HappyLog(log_ini=log_ini)

    hlog.var('args', args)

    # ---------- 建立数据库连接 ----------
    try:
        client = pymongo.MongoClient(mongodb_connection, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        collection = db[collection_name]
    except pymongo.errors.ConfigurationError as e:
        hlog.error(f"MongoDB 连接地址配置有误: {e}")
        sys.exit(1)
    except pymongo.errors.PyMongoError as e:
        hlog.error(f"MongoDB 客户端初始化失败: {e}")
        sys.exit(1)

    # ---------- 执行操作 ----------
    try:
        if args.insert_data:
            inserted_id = insert_document(collection, args.insert_data)
            hlog.info(f"已插入数据，ID: {inserted_id}")

        elif args.search_data is not None:
            if args.search_data:
                try:
                    search_criteria = json.loads(args.search_data)
                except json.JSONDecodeError:
                    hlog.error("查询条件必须为合法的 JSON 格式")
                    sys.exit(1)
                found_documents = find_document(collection, search_criteria)
            else:
                found_documents = find_document(collection, {})

            hlog.info("以下数据已查询：")
            for document in found_documents:
                hlog.info(document)

        elif args.update_data:
            if 'name' not in args.update_data:
                hlog.error("更新数据中必须包含 'name' 字段作为查询条件")
                sys.exit(1)
            update_query = {"name": args.update_data["name"]}
            updated_count = update_document(collection, update_query, args.update_data)
            hlog.info(f"已更新 {updated_count} 条数据")

        elif args.delete_data:
            deleted_count = delete_document(collection, args.delete_data)
            hlog.info(f"已删除 {deleted_count} 条数据")

        elif args.dump_file:
            try:
                dump_data_to_file(collection, args.dump_file)
                hlog.info(f"数据已导出至文件：{args.dump_file}")
            except (PermissionError, OSError) as e:
                hlog.error(str(e))
                sys.exit(1)

        elif args.import_file:
            try:
                success_count, fail_count = import_data_from_file(collection, args.import_file)
                hlog.info(f"导入完成：成功 {success_count} 条，跳过（重复键）{fail_count} 条")
            except (FileNotFoundError, PermissionError, json.JSONDecodeError, OSError) as e:
                hlog.error(str(e))
                sys.exit(1)

        else:
            hlog.error("命令行参数错误，请查看使用说明：")
            parser.print_help()

    except pymongo.errors.ServerSelectionTimeoutError as e:
        hlog.error(str(e))
        sys.exit(1)
    except pymongo.errors.ConnectionFailure as e:
        hlog.error(str(e))
        sys.exit(1)
    except pymongo.errors.DuplicateKeyError as e:
        hlog.error(str(e))
        sys.exit(1)
    except pymongo.errors.OperationFailure as e:
        hlog.error(str(e))
        sys.exit(1)
    except pymongo.errors.PyMongoError as e:
        hlog.error(f"数据库操作发生未知错误: {e}")
        sys.exit(1)
    finally:
        client.close()
