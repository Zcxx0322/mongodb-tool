import json


def export_data_to_file(collection, filename):
    data = list(collection.find({}))
    cleaned_data = []
    for document in data:
        cleaned_document = document.copy()
        cleaned_document['_id'] = str(document['_id'])
        cleaned_data.append(cleaned_document)

    with open(filename, 'w') as file:
        json.dump(cleaned_data, file)


def import_data_from_file(collection, filename):
    with open(filename, 'r') as file:
        data = json.load(file)  # 解析JSON字符串为Python字典
        if isinstance(data, list):
            for document in data:
                collection.insert_one(document)
        else:
            collection.insert_one(data)
