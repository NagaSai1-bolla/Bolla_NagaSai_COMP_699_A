from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from models.user import User

auth_bp = Blueprint('auth', __name__)


# ==============================
# REGISTER
# ==============================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            flash("All fields are required", "danger")
            return redirect(url_for("auth.register"))

        if User.register(name, email, password):
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Email already exists", "danger")

    return render_template("register.html")


# ==============================
# LOGIN
# ==============================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.login(email, password)

        if user:
            # STORE SESSION
            session.clear()
            session["user_id"] = user["id"]
            session["role"] = user["role"]

            flash("Login successful", "success")

            # ROLE-BASED REDIRECT
            if user["role"] == "patient":
                return redirect("/patient/dashboard")
            elif user["role"] == "staff":
                return redirect("/staff/dashboard")
            elif user["role"] == "admin":
                return redirect("/admin/dashboard")

        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")


# ==============================
# LOGOUT
# ==============================
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))


# ==============================
# RESET PASSWORD
# ==============================
@auth_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        new_password = request.form.get("password")

        if not email or not new_password:
            flash("All fields are required", "danger")
            return redirect(url_for("auth.reset_password"))

        User.reset_password(email, new_password)
        flash("Password reset successful", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html")