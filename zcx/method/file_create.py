import os
from importlib.resources import files
from pathlib import Path


def _read_bundled_config():
    """从包内 conf/ 目录读取 config.ini 模板内容。"""
    return (files('zcx') / 'conf' / 'config.ini.sample').read_text(encoding='utf-8')


def _generate_log_ini(config_dir: str) -> str:
    """动态生成 log.ini，将日志文件写入 ~/.zcx/error.log（绝对路径）。"""
    log_file = os.path.join(config_dir, 'error.log').replace('\\', '/')
    return f"""\
[loggers]
keys = root

[formatters]
keys = defaultFormatter

[formatter_defaultFormatter]
format = %(asctime)s %(process)s [%(levelname)s] %(message)s
datefmt = %Y-%m-%d %H:%M:%S
class = logging.Formatter

[handlers]
keys = defaultHandler, fileHandler

[handler_defaultHandler]
class = StreamHandler
level = INFO
formatter = defaultFormatter
args = (sys.stdout,)

[handler_fileHandler]
class = logging.handlers.RotatingFileHandler
level = INFO
formatter = defaultFormatter
args = ('{log_file}', 'a', 100000000, 3, 'utf-8', False)

[logger_root]
level = INFO
handlers = defaultHandler, fileHandler
"""


def create_config_if_not_exists():
    user_config_dir = os.path.join(str(Path.home()), ".zcx")

    if not os.path.exists(user_config_dir):
        os.makedirs(user_config_dir)

    user_config_file = os.path.join(user_config_dir, "config.ini")
    user_log_config_file = os.path.join(user_config_dir, "log.ini")

    if not os.path.exists(user_config_file):
        content = _read_bundled_config()
        with open(user_config_file, 'w', encoding='utf-8') as f:
            f.write(content)

    if not os.path.exists(user_log_config_file):
        content = _generate_log_ini(user_config_dir)
        with open(user_log_config_file, 'w', encoding='utf-8') as f:
            f.write(content)
