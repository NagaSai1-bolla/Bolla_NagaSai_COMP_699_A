from models.queue import Queue


class Patient:

    @staticmethod
    def join_queue(user_id, queue_id):
        return Queue.add_patient(user_id, queue_id)

    @staticmethod
    def leave_queue(user_id, queue_id):
        Queue.remove_patient(user_id, queue_id)

    @staticmethod
    def get_position(user_id, queue_id):
        return Queue.get_position(user_id, queue_id)

    @staticmethod
    def get_wait_time(queue_length, avg_time):
        return queue_length * avg_time