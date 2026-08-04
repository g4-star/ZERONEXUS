from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO

# ==========================================
# Database
# ==========================================

db = SQLAlchemy()

# ==========================================
# Authentication
# ==========================================

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"

# ==========================================
# Database Migrations
# ==========================================

migrate = Migrate()

# ==========================================
# CSRF Protection
# ==========================================

csrf = CSRFProtect()

# ==========================================
# Mail
# ==========================================

mail = Mail()

# ==========================================
# Socket.IO
# ==========================================

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet",
)

# ==========================================
# Rate Limiter
# ==========================================

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/hour"],
    storage_uri="memory://",
)