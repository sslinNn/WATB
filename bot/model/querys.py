from bot.model.connection import get_connetion_with_db
import sqlalchemy as db

def insert_id_and_location_in_db(id_, location_):
    try:
        with get_connetion_with_db().connect() as conn:
            engine = get_connetion_with_db()
            meta = db.MetaData()
            users = db.Table('users', meta, autoload_with=engine)
            conn.execute(users.insert().values([{'id': id_, 'location': location_}]))
            conn.commit()
    except Exception as ex:
        print(ex)

