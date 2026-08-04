import os
from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ======================================================
    # Core Flask Settings
    # ======================================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )

    FLASK_ENV = os.getenv(
        "FLASK_ENV",
        "development"
    )

    # ======================================================
    # Database Configuration
    # ======================================================

    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:

        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1,
            )

        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    else:

        SQLALCHEMY_DATABASE_URI = (
            f"sqlite:///{os.path.join(BASE_DIR, 'zeronexus.db')}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_timeout": 30,
    }

    # ======================================================
    # Cloudinary
    # ======================================================

    CLOUDINARY_CLOUD_NAME = os.getenv(
        "CLOUDINARY_CLOUD_NAME"
    )

    CLOUDINARY_API_KEY = os.getenv(
        "CLOUDINARY_API_KEY"
    )

    CLOUDINARY_API_SECRET = os.getenv(
        "CLOUDINARY_API_SECRET"
    )

    # ======================================================
    # Mail Configuration (Brevo)
    # ======================================================

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp-relay.brevo.com"
    )

    MAIL_PORT = int(
        os.getenv("MAIL_PORT", 587)
    )

    MAIL_USE_TLS = (
        os.getenv(
            "MAIL_USE_TLS",
            "True"
        ).lower() == "true"
    )

    MAIL_USE_SSL = (
        os.getenv(
            "MAIL_USE_SSL",
            "False"
        ).lower() == "true"
    )

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER",
        f"ZeroNexus <{MAIL_USERNAME}>"
    )

    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_MAX_EMAILS = None
    MAIL_DEBUG = True

    # ======================================================
    # Uploads
    # ======================================================

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "app",
        "static",
        "uploads",
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_IMAGE_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp",
    }

    ALLOWED_DOCUMENT_EXTENSIONS = {
        "pdf",
    }

    # ======================================================
    # Session Security
    # ======================================================

    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        os.getenv(
            "SESSION_COOKIE_SECURE",
            "False"
        ).lower() == "true"
    )

    REMEMBER_COOKIE_SECURE = (
        os.getenv(
            "REMEMBER_COOKIE_SECURE",
            "False"
        ).lower() == "true"
    )

    WTF_CSRF_TIME_LIMIT = None

    # ======================================================
    # Administrator
    # ======================================================

    ADMIN_USERNAME = os.getenv(
        "ADMIN_USERNAME"
    )

    ADMIN_EMAIL = os.getenv(
        "ADMIN_EMAIL"
    )

    ADMIN_PASSWORD = os.getenv(
        "ADMIN_PASSWORD"
    )

    # ======================================================
    # Gemini AI
    # ======================================================

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    # ======================================================
    # Public Site URL
    # ======================================================

    SITE_URL = os.getenv(
        "SITE_URL",
        "http://127.0.0.1:5000"
    )


class DevelopmentConfig(Config):

    DEBUG = True


class ProductionConfig(Config):

    DEBUG = False

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}