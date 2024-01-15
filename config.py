import os

class DevelopmentConfig:
    MYSQL_HOST = "192.168.7.195"
    MYSQL_PORT = 4306
    MYSQL_USER = "dev_cag_rwl"
    MYSQL_PASSWD = "7D9gQwpiI8n4TyV"
    MYSQL_DB = "data_pub"

class AliYunConfig:
    MYSQL_HOST = "127.0.0.1"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWD = "7D9gQwpiI8n4TyV_7D9gQwpiI8n4TyV"
    MYSQL_DB = "data_pub"

CONFIG_DICT = {
    'development': DevelopmentConfig(),
    'aliyun': AliYunConfig(),
    'default': DevelopmentConfig(),
}


ENV = os.getenv("ENV", "development")
CONFIG = CONFIG_DICT.get(ENV)

MYSQL_HOST = CONFIG.MYSQL_HOST
MYSQL_PORT = CONFIG.MYSQL_PORT
MYSQL_USER = CONFIG.MYSQL_USER
MYSQL_PASSWD = CONFIG.MYSQL_PASSWD
MYSQL_DB = CONFIG.MYSQL_DB
