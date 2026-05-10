from flask import Blueprint, render_template, request, redirect, session, flash

from models.staff import ServiceStaff
from services.queue_service import QueueService
from services.report_service import ReportService
from database.db import get_db_connection

staff_bp = Blueprint('staff', __name__)


# ==============================
# STAFF DASHBOARD
# ==============================
@staff_bp.route("/staff/dashboard")
def dashboard():
    if session.get("role") != "staff":
        return redirect("/login")

    user_id = session.get("user_id")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get only assigned desk
    cursor.execute("""
        SELECT * FROM service_desks
        WHERE assigned_staff_id = ?
    """, (user_id,))

    desks = cursor.fetchall()
    conn.close()

    return render_template("dashboard_staff.html", desks=desks)


# ==============================
# OPEN DESK
# ==============================
@staff_bp.route("/staff/open/<int:desk_id>")
def open_desk(desk_id):
    if session.get("role") != "staff":
        return redirect("/login")

    ServiceStaff.open_desk(desk_id)

    flash("Desk opened successfully", "success")  # ✅ FLASH

    return redirect("/staff/dashboard")


# ==============================
# PAUSE DESK
# ==============================
@staff_bp.route("/staff/pause/<int:desk_id>")
def pause_desk(desk_id):
    if session.get("role") != "staff":
        return redirect("/login")

    ServiceStaff.pause_desk(desk_id)

    flash("Desk paused", "info")  # ✅ FLASH

    return redirect("/staff/dashboard")


# ==============================
# SERVE NEXT PATIENT
# ==============================
@staff_bp.route("/staff/next/<int:desk_id>")
def next_patient(desk_id):
    if session.get("role") != "staff":
        return redirect("/login")

    user_id = session.get("user_id")

    served = QueueService.serve_next_patient(desk_id, user_id)

    if served:
        flash("Next patient served successfully", "success")  # ✅ FLASH
    else:
        flash("No patients in queue", "info")  # ✅ EDGE CASE

    return redirect("/staff/dashboard")


# ==============================
# REPORT
# ==============================
@staff_bp.route("/staff/report/<int:desk_id>")
def report(desk_id):
    if session.get("role") != "staff":
        return redirect("/login")

    data = ReportService.get_service_summary(desk_id)

    return render_template("reports.html", data=data)


# ==============================
# EXPORT LOGS
# ==============================
@staff_bp.route("/staff/export")
def export():
    if session.get("role") != "staff":
        return redirect("/login")

    ReportService.export_logs_to_csv()

    flash("Logs exported successfully", "success")  

    return redirect("/staff/dashboard")