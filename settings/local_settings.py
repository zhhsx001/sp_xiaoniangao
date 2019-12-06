# coding: utf-8

PORT = 7392


# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/FamilyAs?charset=utf8mb4'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:@127.0.0.1:3306/sp_xiaoniangao?charset=utf8mb4'
SQLALCHEMY_POOL_SIZE = 4
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 3600

REDIS_HOST = '47.98.32.83'
REDIS_PORT = 6379
REDIS_PASS = 'skeweeed'
REDIS_DB = 0

# admin
ADMIN_PORT = 7393

# passport service
PASSPORT_PORT = 7391

SERVICE_SDK_PASSPORT = 'http://127.0.0.1:7391'

