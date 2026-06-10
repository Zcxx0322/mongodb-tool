# zcx — MongoDB 命令行管理工具

通过简单的命令行操作管理 MongoDB 集合，支持增删查改、数据导入导出。

## 安装

推荐使用 [pipx](https://pipx.pypa.io) 安装，安装后可直接使用 `zcx` 命令，无需手动配置 PATH：

```bash
pipx install zcx
```

也可以用 pip 安装，但部分系统（如 Arch Linux）需要手动将 `~/.local/bin` 加入 PATH：

```bash
pip install zcx

# 如果安装后找不到 zcx 命令，执行以下命令（写入 ~/.bashrc 永久生效）：
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

## 快速开始

首次运行任意 `zcx` 命令时，会自动在 `~/.zcx/` 目录下生成配置文件：

```
~/.zcx/
├── config.ini   # 数据库连接配置（需要手动编辑）
└── log.ini      # 日志配置（自动生成，无需修改）
```

编辑 `~/.zcx/config.ini`，填写你的 MongoDB 连接信息：

```ini
[main]
db_url = mongodb://127.0.0.1:27017/
db_name = mydatabase
collection_name = mycollection
```

## 使用说明

```
用法: zcx [-c <配置文件>] [-l <日志配置文件>] [-i <数据>] [-d <条件>]
          [-s [条件]] [-u <数据>] [--dump <文件名>] [--import <文件名>]

选项:
  -h, --help       显示此帮助信息并退出
  -c 配置文件       配置文件路径，默认为 ~/.zcx/config.ini
  -l 日志配置文件   日志配置文件路径，默认为 ~/.zcx/log.ini
  -i 数据          执行插入操作，提供数据（JSON 格式）
  -d 条件          执行删除操作，提供查询条件（JSON 格式）
  -s [条件]        执行查询操作，提供查询条件（JSON 格式），不填条件则查全部
  -u 数据          执行更新操作，提供查询条件和更新数据（JSON 格式）
  --dump 文件名     导出集合数据到指定文件（JSON 格式）
  --import 文件名   从指定文件导入数据到集合（JSON 格式）
```

## 示例

### 插入数据

```bash
zcx -i '{"name": "Alice", "age": 25, "city": "Beijing"}'
```

### 查询数据

```bash
# 查询全部
zcx -s

# 按条件查询
zcx -s '{"name": "Alice"}'
```

### 更新数据

以 `name` 字段作为匹配条件，更新该记录的其他字段：

```bash
zcx -u '{"name": "Alice", "age": 26, "city": "Shanghai"}'
```

### 删除数据

```bash
zcx -d '{"name": "Alice"}'
```

### 导出数据

将集合中所有数据导出为 JSON 文件：

```bash
zcx --dump backup.json
```

### 导入数据

从 JSON 文件批量导入数据（重复键自动跳过）：

```bash
zcx --import backup.json
```

### 使用自定义配置文件

```bash
zcx -c /path/to/config.ini -s
```

## 依赖

- Python >= 3.9
- [pymongo](https://pypi.org/project/pymongo/) >= 4.0
- [happy-python](https://pypi.org/project/happy-python/)

## License

MIT
