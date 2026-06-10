import pymongo.errors


def insert_document(collection, data):
    try:
        result = collection.insert_one(data)
        return result.inserted_id
    except pymongo.errors.DuplicateKeyError as e:
        raise pymongo.errors.DuplicateKeyError(f"插入失败，存在重复键: {e}") from e
    except pymongo.errors.ServerSelectionTimeoutError as e:
        raise pymongo.errors.ServerSelectionTimeoutError(
            f"无法连接到 MongoDB 服务器，请检查服务是否启动及连接地址是否正确: {e}"
        ) from e
    except pymongo.errors.ConnectionFailure as e:
        raise pymongo.errors.ConnectionFailure(f"数据库连接失败: {e}") from e
    except pymongo.errors.OperationFailure as e:
        raise pymongo.errors.OperationFailure(f"插入操作失败（权限或写入错误）: {e}") from e
    except pymongo.errors.PyMongoError as e:
        raise pymongo.errors.PyMongoError(f"插入时发生未知数据库错误: {e}") from e


def find_document(collection, query):
    try:
        result = collection.find(query)
        return list(result)
    except pymongo.errors.ServerSelectionTimeoutError as e:
        raise pymongo.errors.ServerSelectionTimeoutError(
            f"无法连接到 MongoDB 服务器，请检查服务是否启动及连接地址是否正确: {e}"
        ) from e
    except pymongo.errors.ConnectionFailure as e:
        raise pymongo.errors.ConnectionFailure(f"数据库连接失败: {e}") from e
    except pymongo.errors.OperationFailure as e:
        raise pymongo.errors.OperationFailure(f"查询操作失败（权限或查询语法错误）: {e}") from e
    except pymongo.errors.PyMongoError as e:
        raise pymongo.errors.PyMongoError(f"查询时发生未知数据库错误: {e}") from e


def update_document(collection, query, new_data):
    try:
        result = collection.update_many(query, {"$set": new_data})
        return result.modified_count
    except pymongo.errors.ServerSelectionTimeoutError as e:
        raise pymongo.errors.ServerSelectionTimeoutError(
            f"无法连接到 MongoDB 服务器，请检查服务是否启动及连接地址是否正确: {e}"
        ) from e
    except pymongo.errors.ConnectionFailure as e:
        raise pymongo.errors.ConnectionFailure(f"数据库连接失败: {e}") from e
    except pymongo.errors.OperationFailure as e:
        raise pymongo.errors.OperationFailure(f"更新操作失败（权限或写入错误）: {e}") from e
    except pymongo.errors.PyMongoError as e:
        raise pymongo.errors.PyMongoError(f"更新时发生未知数据库错误: {e}") from e


def delete_document(collection, query):
    try:
        result = collection.delete_many(query)
        return result.deleted_count
    except pymongo.errors.ServerSelectionTimeoutError as e:
        raise pymongo.errors.ServerSelectionTimeoutError(
            f"无法连接到 MongoDB 服务器，请检查服务是否启动及连接地址是否正确: {e}"
        ) from e
    except pymongo.errors.ConnectionFailure as e:
        raise pymongo.errors.ConnectionFailure(f"数据库连接失败: {e}") from e
    except pymongo.errors.OperationFailure as e:
        raise pymongo.errors.OperationFailure(f"删除操作失败（权限或写入错误）: {e}") from e
    except pymongo.errors.PyMongoError as e:
        raise pymongo.errors.PyMongoError(f"删除时发生未知数据库错误: {e}") from e
