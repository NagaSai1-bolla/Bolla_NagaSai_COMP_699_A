from database.db import get_db_connection


class NotificationService:

    # ==============================
    # CREATE NOTIFICATION (NO DUPLICATES)
    # ==============================
    @staticmethod
    def create_notification(user_id, message):
        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ CHECK IF SAME MESSAGE ALREADY EXISTS (UNREAD)
        cursor.execute("""
            SELECT id FROM notifications
            WHERE user_id=? AND message=? AND is_read=0
        """, (user_id, message))

        exists = cursor.fetchone()

        # ✅ INSERT ONLY IF NOT EXISTS
        if not exists:
            cursor.execute("""
                INSERT INTO notifications (user_id, message)
                VALUES (?, ?)
            """, (user_id, message))
            conn.commit()

        conn.close()


    # ==============================
    # GET NOTIFICATIONS (UNIQUE + CLEAN)
    # ==============================
    @staticmethod
    def get_notifications(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, message FROM notifications
            WHERE user_id=? AND is_read=0
            ORDER BY created_at DESC
        """, (user_id,))

        rows = cursor.fetchall()

        # ✅ REMOVE DUPLICATES IN DISPLAY
        seen = set()
        unique_notifications = []

        for row in rows:
            msg = row["message"]
            if msg not in seen:
                unique_notifications.append(row)
                seen.add(msg)

        conn.close()

        return unique_notifications


    # ==============================
    # MARK AS READ
    # ==============================
    @staticmethod
    def mark_as_read(notification_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE notifications
            SET is_read=1
            WHERE id=?
        """, (notification_id,))

        conn.commit()
        conn.close()


    # ==============================
    # CLEAR ALL
    # ==============================
    @staticmethod
    def clear_notifications(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM notifications
            WHERE user_id=?
        """, (user_id,))

        conn.commit()
        conn.close()