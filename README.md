# mongodb-tool

mongodb操作工具

## 环境准备

### 安装happy-python & pymongo
```bash
pip install happy-python

python -m pip install "pymongo[srv]" --trusted-host pypi.tuna.tsinghua.edu.cn
```

## 单元测试

## 使用举例

### 增加数据

```bash
python main.py -i '{"name": "John", "age": 30, "city": "New York"}'
```

### 增加数据
```bash
python main.py -i '{"name": "John", "age": 30, "city": "New York"}'
```

### 删除数据
```bash
python main.py -d '{"name": "John", "age": 30, "city": "New York"}'
```

### 查找数据

#### 查找指定键值对数据
```bash
python main.py -s '{"name": "John"}'
```

#### 查找集合中所有数据
```bash
python main.py -s 
```

### 修改数据
```bash
python main.py -u '{"name": "John", "age": 34, "city": "Shanghai"}'
```

## 使用详细
请使用python main.py --help/-h
```
$ python main.py --help
usage: mongodb_tool [-i <data>] [-d <data>] [-s <data>] [-u <data>]

MongoDB工具

options:
  -h, --help        show this help message and exit
  -i INSERT_DATA    执行插入操作，提供数据（JSON格式）
  -d DELETE_DATA    执行删除操作，提供查询条件（JSON格式）
  -s [SEARCH_DATA]  执行查询操作，提供查询条件（JSON格式）
  -u UPDATE_DATA    执行更新操作，提供查询条件和更新数据（JSON格式）
```
