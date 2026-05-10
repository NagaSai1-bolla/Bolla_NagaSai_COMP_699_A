from database.db import get_db_connection


class ServiceDesk:

    @staticmethod
    def get_all_desks():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM service_desks")
        desks = cursor.fetchall()

        conn.close()
        return desks

    @staticmethod
    def get_open_desks():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM service_desks WHERE is_open=1
        """)
        desks = cursor.fetchall()

        conn.close()
        return desks

    @staticmethod
    def get_desk(desk_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM service_desks WHERE id=?
        """, (desk_id,))

        desk = cursor.fetchone()
        conn.close()

        return desk