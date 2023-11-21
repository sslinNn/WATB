import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()


def get_connetion_with_db():
    user_ = os.getenv('user')
    passwd_ = os.getenv('passwd')
    host_ = os.getenv('host')
    dbname_ = os.getenv('dbname')
    try:
        engine = create_engine(
            f'mysql+mysqlconnector://{user_}:{passwd_}@{host_}/{dbname_}',
            pool_size=10,
            max_overflow=20
        )
        return engine
    except Exception as ex:
        return ex


if __name__ == '__main__':
    print(get_connetion_with_db())
