from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash

from models.admin import SystemAdministrator
from services.report_service import ReportService
from database.db import get_db_connection

admin_bp = Blueprint('admin', __name__)


# ==============================
# ADMIN DASHBOARD
# ==============================
@admin_bp.route("/admin/dashboard")
def dashboard():
    if session.get("role") != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch desks with assigned staff name
    cursor.execute("""
        SELECT sd.id, sd.desk_type, sd.is_open,
               u.name AS staff_name
        FROM service_desks sd
        LEFT JOIN users u ON sd.assigned_staff_id = u.id
    """)
    desks = cursor.fetchall()

    # Fetch all staff
    cursor.execute("""
        SELECT id, name FROM users WHERE role='staff'
    """)
    staff = cursor.fetchall()

    conn.close()

    report = ReportService.generate_admin_report()

    return render_template(
        "dashboard_admin.html",
        desks=desks,
        staff=staff,
        report=report
    )


# ==============================
# CREATE SERVICE DESK
# ==============================
@admin_bp.route("/admin/create_desk", methods=["POST"])
def create_desk():
    if session.get("role") != "admin":
        return redirect("/login")

    desk_type = request.form.get("desk_type")

    if not desk_type:
        flash("Desk name is required", "danger")
        return redirect("/admin/dashboard")

    SystemAdministrator.create_desk(desk_type)

    flash("Service desk created successfully", "success")
    return redirect("/admin/dashboard")


# ==============================
# CREATE STAFF
# ==============================
@admin_bp.route("/admin/create_staff", methods=["POST"])
def create_staff():
    if session.get("role") != "admin":
        return redirect("/login")

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        flash("All fields are required", "danger")
        return redirect("/admin/dashboard")

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, 'staff')
        """, (name, email, hashed_password))

        conn.commit()
        flash("Staff created successfully", "success")

    except Exception:
        flash("Email already exists", "danger")

    finally:
        conn.close()

    return redirect("/admin/dashboard")


# ==============================
# ASSIGN STAFF TO DESK
# ==============================
@admin_bp.route("/admin/assign", methods=["POST"])
def assign():
    if session.get("role") != "admin":
        return redirect("/login")

    desk_id = request.form.get("desk_id")
    staff_id = request.form.get("staff_id")

    if not desk_id or not staff_id:
        flash("Please select both desk and staff", "danger")
        return redirect("/admin/dashboard")

    SystemAdministrator.assign_staff(desk_id, staff_id)

    flash("Staff assigned to desk successfully", "success")
    return redirect("/admin/dashboard")


# ==============================
# TRAIN ML MODEL
# ==============================
@admin_bp.route("/admin/train")
def train_model():
    if session.get("role") != "admin":
        return redirect("/login")

    try:
        from ml.train_model import train_model
        train_model()
        flash("ML model trained successfully", "success")
    except Exception:
        flash("Error training model", "danger")

    return redirect("/admin/dashboard")