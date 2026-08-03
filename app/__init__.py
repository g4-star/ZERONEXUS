import os

from flask import Flask, render_template

from config import config_map

from app.extensions import (
    db,
    login_manager,
    migrate,
    csrf,
    limiter,
    mail,
    socketio,
)

from app.cloudinary_config import configure_cloudinary
from app.academy import academy


def create_app(config_name=None):
    """Application factory for ZeroNexus."""

    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(
        config_map.get(config_name, config_map["default"])
    )

    # ----------------------------------
    # Cloudinary
    # ----------------------------------

    with app.app_context():
        configure_cloudinary()

    # ----------------------------------
    # Local upload directories
    # ----------------------------------

    if not os.environ.get("VERCEL"):
        os.makedirs(app.instance_path, exist_ok=True)

        for folder in (
            "members",
            "teams",
            "projects",
            "blog",
            "avatars",
        ):
            os.makedirs(
                os.path.join(
                    app.root_path,
                    "static",
                    "uploads",
                    folder,
                ),
                exist_ok=True,
            )

    # ----------------------------------
    # Extensions
    # ----------------------------------

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    socketio.init_app(app)

    # ----------------------------------
    # Blueprints
    # ----------------------------------

    from app.main import main_bp
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.user import user_bp
    from app.team import team_bp

    from app.api.chat import chat_api
    from app.api.dashboard import dashboard_api

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(academy)

    app.register_blueprint(chat_api)
    app.register_blueprint(dashboard_api)

    # ----------------------------------
    # Optional AI Blueprint
    # ----------------------------------

    try:
        from app.ai import ai_bp

        app.register_blueprint(ai_bp)

    except ImportError:
        pass

    # ----------------------------------
    # Security Headers
    # ----------------------------------

    @app.after_request
    def security_headers(response):
        response.headers.setdefault(
            "X-Content-Type-Options",
            "nosniff",
        )

        response.headers.setdefault(
            "X-Frame-Options",
            "DENY",
        )

        response.headers.setdefault(
            "Referrer-Policy",
            "strict-origin-when-cross-origin",
        )

        response.headers.setdefault(
            "Permissions-Policy",
            "camera=(), microphone=(), geolocation=()",
        )

        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; "
            "img-src 'self' data: https:; "
            "style-src 'self' 'unsafe-inline' https:; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "font-src 'self' https:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none'",
        )

        return response

    # ----------------------------------
    # Error Handlers
    # ----------------------------------

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # ----------------------------------
    # Flask Shell
    # ----------------------------------

    @app.shell_context_processor
    def make_shell_context():
        from app.models import (
            Team,
            MemberProfile,
            Project,
            User,
        )

        from app.models.course import Course
        from app.models.lesson import Lesson
        from app.models.progress import UserProgress

        return {
            "db": db,
            "Team": Team,
            "MemberProfile": MemberProfile,
            "Project": Project,
            "User": User,
            "Course": Course,
            "Lesson": Lesson,
            "UserProgress": UserProgress,
        }

    return app