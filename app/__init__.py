import os
from flask import Flask, render_template
from config import config_map

from app.extensions import (
    db,
    login_manager,
    migrate,
    csrf,
    limiter,
    mail
)

from app.cloudinary_config import configure_cloudinary


def create_app(config_name=None):
    """Application factory for ZeroNexus."""

    # -------------------------------------------------
    # Determine environment configuration
    # -------------------------------------------------
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__, instance_relative_config=True)

    # -------------------------------------------------
    # Load configuration
    # -------------------------------------------------
    app.config.from_object(
        config_map.get(config_name, config_map["default"])
    )

    # -------------------------------------------------
    # Configure Cloudinary
    # -------------------------------------------------
    with app.app_context():
        configure_cloudinary()

    # -------------------------------------------------
    # Skip directory creation on Vercel
    # -------------------------------------------------
    if not os.environ.get("VERCEL"):

        os.makedirs(app.instance_path, exist_ok=True)

        upload_root = os.path.join(
            app.root_path,
            "static",
            "uploads"
        )

        os.makedirs(upload_root, exist_ok=True)
        os.makedirs(os.path.join(upload_root, "members"), exist_ok=True)
        os.makedirs(os.path.join(upload_root, "teams"), exist_ok=True)
        os.makedirs(os.path.join(upload_root, "projects"), exist_ok=True)
        os.makedirs(os.path.join(upload_root, "blog"), exist_ok=True)
        os.makedirs(os.path.join(upload_root, "avatars"), exist_ok=True)

    # -------------------------------------------------
    # Initialize Extensions
    # -------------------------------------------------
    db.init_app(app)

    login_manager.init_app(app)

    migrate.init_app(app, db)

    csrf.init_app(app)

    mail.init_app(app)

    limiter.init_app(app)

    # -------------------------------------------------
    # Register Blueprints
    # -------------------------------------------------
    from app.main import main_bp
    from app.admin import admin_bp

    app.register_blueprint(main_bp)

    app.register_blueprint(admin_bp)

    # -------------------------------------------------
    # Error Handlers
    # -------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # -------------------------------------------------
    # Flask Shell
    # -------------------------------------------------
    @app.shell_context_processor
    def make_shell_context():
        from app.models import (
            Team,
            MemberProfile,
            Project,
            AdminUser
        )

        return {
            "db": db,
            "Team": Team,
            "MemberProfile": MemberProfile,
            "Project": Project,
            "AdminUser": AdminUser,
        }

    return app