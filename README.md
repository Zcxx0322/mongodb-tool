# mongodb-tool

mongodb操作工具

## 环境准备

```bash
pip install happy-python pymongo
```

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
```bash
python main.py -s '{"name": "John"}'

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
2023-10-05 17:25:30 20519 [INFO] 未启用日志配置文件，加载默认设置
2023-10-05 17:25:30 20519 [INFO] 日志配置文件 '/home/colamps/.zcx/log.ini' 加载成功
2023-10-05 17:25:30 20519 [ERROR] 命令行参数错误，请查看使用说明：
usage: mongodb_tool [-c <config_file>] [-l <log_config_file>][-i <data>] [-d <data>] [-s <data>] [-u <data>] [--dump <filename>] [--import <filename>]

MongoDB工具

options:
  -h, --help            show this help message and exit
  -c CONFIG_FILE        配置文件路径，默认为 ~/.zcx/config.ini
  -l LOG_CONFIG_FILE    日志配置文件路径，默认为 ~/.zcx/log.ini
  -i INSERT_DATA        执行插入操作，提供数据（JSON格式）
  -d DELETE_DATA        执行删除操作，提供查询条件（JSON格式）
  -s [SEARCH_DATA]      执行查询操作，提供查询条件（JSON格式）
  -u UPDATE_DATA        执行更新操作，提供查询条件和更新数据（JSON格式）
  --dump DUMP_FILE      导出数据到指定文件（JSON格式）
  --import IMPORT_FILE  从指定文件导入数据（JSON格式）

```