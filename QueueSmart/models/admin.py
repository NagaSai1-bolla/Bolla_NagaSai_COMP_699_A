from database.db import get_db_connection


class SystemAdministrator:

    @staticmethod
    def create_desk(desk_type):
        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ Avoid duplicate desks
        cursor.execute("""
            SELECT id FROM service_desks WHERE desk_type=?
        """, (desk_type,))
        existing = cursor.fetchone()

        if existing:
            conn.close()
            return

        cursor.execute("""
            INSERT INTO service_desks (desk_type, is_open)
            VALUES (?, 0)
        """, (desk_type,))

        desk_id = cursor.lastrowid

        # Create queue automatically
        cursor.execute("""
            INSERT INTO queues (desk_id, current_size)
            VALUES (?, 0)
        """, (desk_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def assign_staff(desk_id, staff_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE service_desks
            SET assigned_staff_id=?
            WHERE id=?
        """, (staff_id, desk_id))

        conn.commit()
        conn.close()