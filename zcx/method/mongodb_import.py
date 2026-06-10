import json

import pymongo.errors


def import_data_from_file(collection, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"导入文件不存在: '{filename}'") from e
    except PermissionError as e:
        raise PermissionError(f"无读取权限，无法打开文件 '{filename}': {e}") from e
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"文件 '{filename}' 不是合法的 JSON 格式: {e.msg}", e.doc, e.pos
        ) from e
    except OSError as e:
        raise OSError(f"读取文件 '{filename}' 失败: {e}") from e

    documents = data if isinstance(data, list) else [data]
    success_count = 0
    fail_count = 0

    for i, document in enumerate(documents):
        try:
            collection.insert_one(document)
            success_count += 1
        except pymongo.errors.DuplicateKeyError:
            fail_count += 1
        except pymongo.errors.ServerSelectionTimeoutError as e:
            raise pymongo.errors.ServerSelectionTimeoutError(
                f"无法连接到 MongoDB 服务器，导入在第 {i + 1} 条记录时中止: {e}"
            ) from e
        except pymongo.errors.ConnectionFailure as e:
            raise pymongo.errors.ConnectionFailure(
                f"数据库连接断开，导入在第 {i + 1} 条记录时中止: {e}"
            ) from e
        except pymongo.errors.OperationFailure as e:
            raise pymongo.errors.OperationFailure(
                f"第 {i + 1} 条记录写入失败（权限或格式错误）: {e}"
            ) from e
        except pymongo.errors.PyMongoError as e:
            raise pymongo.errors.PyMongoError(
                f"导入第 {i + 1} 条记录时发生未知数据库错误: {e}"
            ) from e

    return success_count, fail_count
