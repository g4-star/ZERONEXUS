from flask import request
from flask_login import LoginManager, current_user
from flask_limiter import Limiter
from flask_mail import Mail
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# ==========================================================
# DATABASE
# ==========================================================

db = SQLAlchemy()

# ==========================================================
# AUTHENTICATION
# ==========================================================

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"

# ==========================================================
# DATABASE MIGRATIONS
# ==========================================================

migrate = Migrate()

# ==========================================================
# CSRF PROTECTION
# ==========================================================

csrf = CSRFProtect()

# ==========================================================
# EMAIL
# ==========================================================

mail = Mail()

# ==========================================================
# SOCKET.IO
# ==========================================================

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet",
)

# ==========================================================
# RATE LIMITING
# ==========================================================

def rate_limit_key():
    """
    Use authenticated user ID when available.
    Fall back to client IP for anonymous users.
    """

    if current_user.is_authenticated:
        return f"user:{current_user.id}"

    return request.remote_addr


limiter = Limiter(
    key_func=rate_limit_key,

    # Global default limits
    default_limits=[
        "100 per hour",
        "1000 per day",
    ],

    storage_uri="memory://",
)

# ==========================================================
# LOGIN MANAGER
# ==========================================================

@login_manager.user_loader
def load_user(user_id):
    """
    Import here to avoid circular imports.
    """

    from app.models.user import User

    return User.query.get(int(user_id))