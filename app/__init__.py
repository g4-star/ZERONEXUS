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


def create_app(config_name=None):
    """Application factory for ZeroNexus."""

    # Determine environment configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__, instance_relative_config=True)

    # Load configuration
    app.config.from_object(
        config_map.get(config_name, config_map['default'])
    )

    # Ensure instance folder exists
    if not os.environ.get("VERCEL"):
        os.makedirs(app.instance_path, exist_ok=True)

    # Ensure upload directories exist
    os.makedirs(
        os.path.join(app.root_path, 'static', 'uploads'),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(app.root_path, 'static', 'uploads', 'members'),
        exist_ok=True
    )

    os.makedirs(
        os.path.join(app.root_path, 'static', 'uploads', 'teams'),
        exist_ok=True
    )

    # -------------------------------------------------
    # Initialize Flask extensions
    # -------------------------------------------------
    db.init_app(app)

    login_manager.init_app(app)

    migrate.init_app(app, db)

    csrf.init_app(app)

    mail.init_app(app)

    limiter.init_app(app)

    # -------------------------------------------------
    # Register blueprints
    # -------------------------------------------------
    from app.main import main_bp
    from app.admin import admin_bp

    app.register_blueprint(main_bp)

    app.register_blueprint(admin_bp)

    # -------------------------------------------------
    # Error handlers
    # -------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # -------------------------------------------------
    # Shell context (flask shell)
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
            'db': db,
            'Team': Team,
            'MemberProfile': MemberProfile,
            'Project': Project,
            'AdminUser': AdminUser,
        }

    return app