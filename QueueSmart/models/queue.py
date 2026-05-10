from database.db import get_db_connection


class Queue:

    @staticmethod
    def get_queue_by_desk(desk_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM queues WHERE desk_id = ?", (desk_id,))
        queue = cursor.fetchone()

        conn.close()
        return queue

    @staticmethod
    def create_queue(desk_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO queues (desk_id, current_size)
            VALUES (?, 0)
        """, (desk_id,))

        conn.commit()
        conn.close()

    @staticmethod
    def add_patient(user_id, queue_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MAX(position) FROM queue_entries
            WHERE queue_id = ? AND status = 'waiting'
        """, (queue_id,))
        max_pos = cursor.fetchone()[0]

        new_position = 1 if max_pos is None else max_pos + 1

        cursor.execute("""
            INSERT INTO queue_entries (user_id, queue_id, position, status)
            VALUES (?, ?, ?, 'waiting')
        """, (user_id, queue_id, new_position))

        cursor.execute("""
            UPDATE queues SET current_size = current_size + 1
            WHERE id = ?
        """, (queue_id,))

        conn.commit()
        conn.close()

        return new_position

    @staticmethod
    def remove_patient(user_id, queue_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE queue_entries
            SET status = 'completed'
            WHERE user_id = ? AND queue_id = ? AND status = 'waiting'
        """, (user_id, queue_id))

        cursor.execute("""
            UPDATE queues
            SET current_size = CASE WHEN current_size > 0 THEN current_size - 1 ELSE 0 END
            WHERE id = ?
        """, (queue_id,))

        conn.commit()
        conn.close()

        Queue.reorder_queue(queue_id)

    @staticmethod
    def reorder_queue(queue_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM queue_entries
            WHERE queue_id = ? AND status = 'waiting'
            ORDER BY position
        """, (queue_id,))

        rows = cursor.fetchall()

        for index, row in enumerate(rows, start=1):
            cursor.execute("""
                UPDATE queue_entries
                SET position = ?
                WHERE id = ?
            """, (index, row["id"]))

        conn.commit()
        conn.close()

    @staticmethod
    def get_position(user_id, queue_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT position FROM queue_entries
            WHERE user_id = ? AND queue_id = ? AND status = 'waiting'
        """, (user_id, queue_id))

        result = cursor.fetchone()
        conn.close()

        return result["position"] if result else None

    @staticmethod
    def get_queue_length(queue_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM queue_entries
            WHERE queue_id = ? AND status = 'waiting'
        """, (queue_id,))

        count = cursor.fetchone()[0]
        conn.close()

        return count