import os
from sqlalchemy import create_engine
from dotenv import load_dotenv


def get_connetion_with_db():
    load_dotenv()
    user_ = os.getenv('user')
    passwd_ = os.getenv('passwd')
    host_ = os.getenv('host')
    dbname_ = os.getenv('dbname')
    engine = create_engine(f'mysql+mysqlconnector://{user_}:{passwd_}@{host_}/{dbname_}')
    return engine



if __name__ == "__main__":
    get_connetion_with_db()
