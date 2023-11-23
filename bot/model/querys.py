import sqlalchemy

from bot.model.connection import get_connetion_with_db
import sqlalchemy as db
from datetime import datetime


class Request:
    def __init__(self, conn: sqlalchemy.Connection):
        self.conn = conn


    async def insert_id_and_location_in_db(self, id_, location_):
        try:
            query = db.text("""
                            INSERT INTO users (id, location)
                            VALUES (:id, :location)
                            ON DUPLICATE KEY UPDATE location = :location
                        """)
            self.conn.execute(query, {'id': id_, 'location': location_})
            self.conn.commit()
        except Exception as ex:
            print(ex)


def select_location_from_db(id_):
    try:
        with get_connetion_with_db().connect() as conn:
            engine = get_connetion_with_db()
            meta = db.MetaData()
            users = db.Table('users', meta, autoload_with=engine)
            query = db.select(users.c.location).where(users.c.id == id_)
            result = conn.execute(query)
            return result.fetchone()[0]
    except Exception as ex:
        print(ex)


def insert_id_and_location_in_db_original(id_, location_):
    try:
        with get_connetion_with_db().connect() as conn:
            engine = get_connetion_with_db()
            meta = db.MetaData()
            users = db.Table('users', meta, autoload_with=engine)
            query = db.text("""
                            INSERT INTO users (id, location)
                            VALUES (:id, :location)
                            ON DUPLICATE KEY UPDATE location = :location
                        """)
            conn.execute(query, {'id': id_, 'location': location_})
            conn.commit()
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    print(insert_id_and_location_in_db(666, 'hell'))
