import os

import pymysql
from dotenv import load_dotenv

load_dotenv()
user = os.getenv('user')
passwd = os.getenv('passwd')
host = os.getenv('host')
dbname = os.getenv('dbname')

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=passwd,
        database=dbname,
        cursorclass=pymysql.cursors.DictCursor
    )
    print('DB connected!')
except Exception as ex:
    print('Connection failed!')
    print(ex)
