from database.db import get_db_connection
import csv


class ReportService:

    @staticmethod
    def get_queue_volume(desk_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM queue_entries
            WHERE queue_id = (
                SELECT id FROM queues WHERE desk_id=?
            )
        """, (desk_id,))

        count = cursor.fetchone()[0]
        conn.close()

        return count

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

        return round(avg, 2) if avg else 0

    @staticmethod
    def get_daily_throughput(desk_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM service_logs
            WHERE desk_id=?
        """, (desk_id,))

        count = cursor.fetchone()[0]
        conn.close()

        return count

    @staticmethod
    def get_service_summary(desk_id):
        return {
            "throughput": ReportService.get_daily_throughput(desk_id),
            "avg_time": ReportService.get_avg_service_time(desk_id)
        }

    @staticmethod
    def generate_admin_report():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT desk_id, COUNT(*) as total
            FROM service_logs GROUP BY desk_id
        """)

        data = cursor.fetchall()
        conn.close()

        return data

    @staticmethod
    def export_logs_to_csv(filename="service_logs.csv"):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM service_logs")
        rows = cursor.fetchall()

        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Staff", "Desk", "Time", "Date"])

            for row in rows:
                writer.writerow(row)

        conn.close()

        return filename