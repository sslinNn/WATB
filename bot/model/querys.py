from bot.model.connection import get_connetion_with_db
from sqlalchemy.dialects.mysql import insert

def insert_id_and_location_in_db(id_, location_):
    try:
        with get_connetion_with_db() as conn:
            meta =
            sql1 = insert(users).values
            sql = "INSERT INTO `users` (`id`, `location`) VALUES (%s, %s)"
            conn.execute(sql, (id_, location_))
            conn.commit()
    except Exception as ex:
        print(ex)

# def get_location_from_db():
#     try:
#         with get_connetion_with_db() as conn:
#             sql = "INSERT INTO `users` (`id`, `location`) VALUES (%s, %s)"
#             conn.cursor().execute(sql, (id_, location_))
#             conn.commit()
#     except Exception as ex:
#         print(ex)

