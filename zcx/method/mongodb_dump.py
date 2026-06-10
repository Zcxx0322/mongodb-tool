import json

import pymongo.errors


def dump_data_to_file(collection, filename):
    try:
        data = list(collection.find({}))
    except pymongo.errors.ServerSelectionTimeoutError as e:
        raise pymongo.errors.ServerSelectionTimeoutError(
            f"无法连接到 MongoDB 服务器，导出失败: {e}"
        ) from e
    except pymongo.errors.ConnectionFailure as e:
        raise pymongo.errors.ConnectionFailure(f"数据库连接失败，导出中止: {e}") from e
    except pymongo.errors.OperationFailure as e:
        raise pymongo.errors.OperationFailure(f"读取集合数据失败（权限不足）: {e}") from e
    except pymongo.errors.PyMongoError as e:
        raise pymongo.errors.PyMongoError(f"导出时发生未知数据库错误: {e}") from e

    cleaned_data = []
    for document in data:
        cleaned_document = document.copy()
        cleaned_document['_id'] = str(document['_id'])
        cleaned_data.append(cleaned_document)

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(cleaned_data, file, ensure_ascii=False, indent=2)
    except PermissionError as e:
        raise PermissionError(f"无写入权限，无法创建文件 '{filename}': {e}") from e
    except OSError as e:
        raise OSError(f"写入文件 '{filename}' 失败: {e}") from e
