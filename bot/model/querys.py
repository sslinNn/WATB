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

    async def insert_role_in_db(self, id_, role):
        try:
            query = db.text("""
            INSERT INTO users (id, role)
            VALUES (:id, :role)
            ON DUPLICATE KEY UPDATE role = :role
            """)
            self.conn.execute(query, {'id': id_, 'role': role})
            self.conn.commit()
        except Exception as e:
            print(e)

    async def insert_code_in_db(self, id_):
        try:
            query = db.text("""
                                        INSERT INTO users (id, code_nhtk)
                                        VALUES (:id, 1)
                                        ON DUPLICATE KEY UPDATE code_nhtk = 1
                                    """)
            self.conn.execute(query, {'id': id_})
            self.conn.commit()
        except Exception as e:
            print(e)

    async def insert_group_in_db(self, id_, group):
        try:
            query = db.text("""
                                        INSERT INTO users (id, class_identifier)
                                        VALUES (:id, :class_identifier)
                                        ON DUPLICATE KEY UPDATE class_identifier = :class_identifier
                                    """)
            self.conn.execute(query, {'id': id_, 'class_identifier': group})
            self.conn.commit()
        except Exception as e:
            print(e)

    async def select_code_in_db(self, id_):
        try:
            query = db.text("""
                                                    SELECT code_nhtk
                                                    FROM users
                                                    WHERE id = :id
                                                """)
            result = self.conn.execute(query, {'id': id_})
            print(result)
            return result.fetchone()[0]
        except Exception as e:
            print(e)

    async def select_class_in_db(self, id_):
        try:
            query = db.text("""
                                                    SELECT class_identifier
                                                    FROM users
                                                    WHERE id = :id
                                                """)
            result = self.conn.execute(query, {'id': id_})
            print(result)
            return result.fetchone()[0]
        except Exception as e:
            print(e)

    async def select_role_in_db(self, id_):
        try:
            query = db.text("""
                                                    SELECT role
                                                    FROM users
                                                    WHERE id = :id
                                                """)
            result = self.conn.execute(query, {'id': id_})
            print(result)
            return result.fetchone()[0]
        except Exception as e:
            print(e)

    async def insert_notofication_time(self, id_, notification_time):
        try:
            query = db.text(
                """
                INSERT INTO users (id, notification_time)
                VALUES (:id, :notification_time)
                ON DUPLICATE KEY UPDATE notification_time = :notification_time
                """
            )
            self.conn.execute(query, {'id': id_, 'notification_time': notification_time})
            self.conn.commit()
        except Exception as e:
            print(e)




    async def select_notofication_time_from_db_by_id(self, id_):
        try:
            query = db.text("""
                                                    SELECT notofication_time
                                                    FROM users
                                                    WHERE id = :id
                                                """)
            result = self.conn.execute(query, {'id': id_})
            print(result)
            return result.fetchone()[0]
        except Exception as e:
            print(e)


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
    db = Request(request).insert_notofication_time(id_=123, notification_time='08:40:00')
    # print(insert_not(666, 'hell'))
