from bot.model.connection import get_connetion_with_db

def insert_id_and_location_in_db(id_, location_):
    try:
        with get_connetion_with_db() as conn:
            sql = "INSERT IGNORE INTO `users` (`id`, `location`) VALUES (%s, %s)"
            conn.cursor().execute(sql, (id_, location_))
            conn.commit()
    except Exception as ex:
        print(ex)
