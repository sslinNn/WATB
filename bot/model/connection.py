import os
import pymysql.cursors
from dotenv import load_dotenv
from sqlalchemy import create_engine
import mysql.connector

load_dotenv()


def get_connetion_with_db():
    user_ = os.getenv('user')
    passwd_ = os.getenv('passwd')
    host_ = os.getenv('host')
    dbname_ = os.getenv('dbname')
    try:
        connection = create_engine(
            f'mysql+mysqlconnector://{user_}:{passwd_}@{host_}/{dbname_}'
        )
        return connection.connect()
    except Exception as ex:
        return ex


# def get_connetion_with_db():
#     user_ = os.getenv('user')
#     passwd_ = os.getenv('passwd')
#     host_ = os.getenv('host')
#     dbname_ = os.getenv('dbname')
#     try:
#         connection = pymysql.connect(
#             host=host_,
#             user=user_,
#             password=passwd_,
#             database=dbname_,
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         return connection
#     except Exception as ex:
#         return ex


if __name__ == '__main__':
    print(get_connetion_with_db())
