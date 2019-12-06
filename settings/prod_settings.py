# coding: utf-8

PORT = 7492

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:KingMa!@!2018@rm-bp131gz8co191q243so.mysql.rds.aliyuncs.com:3306/famliyas?charset=utf8mb4'
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 3600

REDIS_HOST = '172.17.57.101'
REDIS_PORT = 6379
REDIS_PASS = 'KingMaSports!@!2018'
REDIS_DB = 0

# admin
ADMIN_PORT = 7393

# passport service
PASSPORT_PORT = 7391

SERVICE_SDK_PASSPORT = 'http://127.0.0.1:7391'
