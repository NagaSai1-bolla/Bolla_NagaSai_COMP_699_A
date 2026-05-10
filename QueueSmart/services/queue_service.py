from models.queue import Queue
from models.service_desk import ServiceDesk
from models.staff import ServiceStaff
from models.ml_engine import WaitingTimeMLEngine
from services.notification_service import NotificationService
import config


class QueueService:

    @staticmethod
    def join_queue(user_id, desk_id):
        queue = Queue.get_queue_by_desk(desk_id)

        if not queue:
            Queue.create_queue(desk_id)
            queue = Queue.get_queue_by_desk(desk_id)

        # PREVENT DUPLICATE ENTRY (IMPORTANT FIX)
        existing_position = Queue.get_position(user_id, queue["id"])
        if existing_position:
            return existing_position

        position = Queue.add_patient(user_id, queue["id"])
        return position

    @staticmethod
    def leave_queue(user_id, desk_id):
        queue = Queue.get_queue_by_desk(desk_id)
        if queue:
            Queue.remove_patient(user_id, queue["id"])

    @staticmethod
    def get_patient_status(user_id, desk_id):
        queue = Queue.get_queue_by_desk(desk_id)
        if not queue:
            return None

        queue_id = queue["id"]

        position = Queue.get_position(user_id, queue_id)
        if position is None:
            return None

        queue_length = Queue.get_queue_length(queue_id)

        avg_time = ServiceStaff.get_avg_service_time(desk_id) or 5

        predicted_wait = WaitingTimeMLEngine.predict(queue_length, avg_time)

        arrival_time = QueueService.calculate_arrival_window(predicted_wait)

        # NOTIFICATION LOGIC
        if position <= config.ALERT_POSITION:
            NotificationService.create_notification(
                user_id, "Your turn is near. Please arrive!"
            )

        return {
            "position": position,
            "queue_length": queue_length,
            "predicted_wait": round(predicted_wait, 2),
            "arrival_window": arrival_time
        }

    @staticmethod
    def calculate_arrival_window(predicted_wait):
        return f"Arrive in approx {int(predicted_wait)} minutes"

    @staticmethod
    def serve_next_patient(desk_id, staff_id):
        queue = Queue.get_queue_by_desk(desk_id)
        if not queue:
            return None

        queue_id = queue["id"]

        served_user = ServiceStaff.serve_next(queue_id, staff_id, desk_id)

        if served_user:
            Queue.reorder_queue(queue_id)

        return served_user