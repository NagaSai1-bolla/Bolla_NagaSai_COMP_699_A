from flask import Flask, render_template, session
from database.db import init_db
import config

# Import Blueprints
from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp
from routes.staff_routes import staff_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)

    # ==============================
    # CONFIGURATION
    # ==============================
    app.config['SECRET_KEY'] = config.SECRET_KEY

    # ==============================
    # INITIALIZE DATABASE
    # ==============================
    init_db()

    # ==============================
    # REGISTER BLUEPRINTS
    # ==============================
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(admin_bp)

    # ==============================
    # GLOBAL USER SESSION ACCESS (VERY IMPORTANT)
    # ==============================
    @app.context_processor
    def inject_user():
        return dict(
            current_user_id=session.get("user_id"),
            current_user_role=session.get("role")
        )

    # ==============================
    # HOME ROUTE
    # ==============================
    @app.route("/")
    def home():
        return render_template("home.html")

    # ==============================
    # GLOBAL ERROR HANDLER
    # ==============================
    @app.errorhandler(404)
    def not_found(error):
        return render_template("home.html"), 404

    return app


# ==============================
# RUN APPLICATION
# ==============================
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)