from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

db = SQLAlchemy()

login_manager = LoginManager()

socketio = SocketIO(
    cors_allowed_origins="*",
    async_mode="eventlet"
)

# Database
db = SQLAlchemy()

# Authentication
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

# Database migrations
migrate = Migrate()

# CSRF protection
csrf = CSRFProtect()

# Email support
mail = Mail()

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=['100/hour'],
    storage_uri='memory://'
)