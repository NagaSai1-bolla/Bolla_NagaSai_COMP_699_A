from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from services.queue_service import QueueService
from models.service_desk import ServiceDesk
from services.notification_service import NotificationService

patient_bp = Blueprint('patient', __name__)


# ==============================
# PATIENT DASHBOARD
# ==============================
@patient_bp.route("/patient/dashboard")
def dashboard():
    if session.get("role") != "patient":
        return redirect("/login")

    user_id = session.get("user_id")

    desks = ServiceDesk.get_all_desks()
    notifications = NotificationService.get_notifications(user_id)

    # Active queue status
    active_status = []
    for desk in desks:
        status = QueueService.get_patient_status(user_id, desk["id"])
        if status and status["position"] is not None:
            active_status.append({
                "desk": desk,
                "status": status
            })

    return render_template(
        "dashboard_patient.html",
        desks=desks,
        notifications=notifications,
        active_status=active_status
    )


# ==============================
# JOIN QUEUE
# ==============================
@patient_bp.route("/patient/join/<int:desk_id>")
def join_queue(desk_id):
    if session.get("role") != "patient":
        return redirect("/login")

    user_id = session.get("user_id")

    position = QueueService.join_queue(user_id, desk_id)

    if position:
        flash(f"You joined the queue successfully. Your position is {position}", "success")
    else:
        flash("You are already in the queue", "info")

    return redirect(url_for("patient.status", desk_id=desk_id))


# ==============================
# VIEW STATUS
# ==============================
@patient_bp.route("/patient/status/<int:desk_id>")
def status(desk_id):
    if session.get("role") != "patient":
        return redirect("/login")

    user_id = session.get("user_id")

    data = QueueService.get_patient_status(user_id, desk_id)
    desk = ServiceDesk.get_desk(desk_id)

    if not data:
        flash("You are not in this queue", "info")
        return redirect("/patient/dashboard")

    return render_template(
        "queue.html",
        data=data,
        desk=desk,
        desk_id=desk_id
    )


# ==============================
# LEAVE QUEUE
# ==============================
@patient_bp.route("/patient/leave/<int:desk_id>")
def leave_queue(desk_id):
    if session.get("role") != "patient":
        return redirect("/login")

    user_id = session.get("user_id")

    QueueService.leave_queue(user_id, desk_id)

    flash("You have left the queue", "info")  # FLASH

    return redirect("/patient/dashboard")


# ==============================
# REFRESH STATUS
# ==============================
@patient_bp.route("/patient/refresh/<int:desk_id>")
def refresh(desk_id):
    return redirect(url_for("patient.status", desk_id=desk_id))