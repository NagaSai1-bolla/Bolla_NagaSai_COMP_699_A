from database.db import get_db_connection
import time


class ServiceStaff:

    @staticmethod
    def open_desk(desk_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE service_desks SET is_open=1 WHERE id=?", (desk_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def pause_desk(desk_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE service_desks SET is_open=0 WHERE id=?", (desk_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def serve_next(queue_id, staff_id, desk_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        # GET NEXT PATIENT
        cursor.execute("""
            SELECT * FROM queue_entries
            WHERE queue_id=? AND status='waiting'
            ORDER BY position LIMIT 1
        """, (queue_id,))
        patient = cursor.fetchone()

        if not patient:
            conn.close()
            return None

        start_time = time.time()

        # MARK COMPLETED
        cursor.execute("""
            UPDATE queue_entries SET status='completed'
            WHERE id=?
        """, (patient["id"],))

        # UPDATE QUEUE SIZE
        cursor.execute("""
            UPDATE queues
            SET current_size = CASE WHEN current_size > 0 THEN current_size - 1 ELSE 0 END
            WHERE id=?
        """, (queue_id,))

        end_time = time.time()
        service_time = end_time - start_time

        # INSERT LOG
        cursor.execute("""
            INSERT INTO service_logs (staff_id, desk_id, service_time)
            VALUES (?, ?, ?)
        """, (staff_id, desk_id, service_time))

        conn.commit()
        conn.close()

        return patient["user_id"]

    @staticmethod
    def get_avg_service_time(desk_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT AVG(service_time) FROM service_logs
            WHERE desk_id=?
        """, (desk_id,))

        avg = cursor.fetchone()[0]
        conn.close()

        return avg if avg else 5