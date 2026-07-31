import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # -------------------------------------------------
    # Core Flask Settings
    # -------------------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # -------------------------------------------------
    # Database Configuration
    # -------------------------------------------------
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        # Some providers still use postgres://
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1,
            )

        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    else:
        # Local SQLite database
        SQLALCHEMY_DATABASE_URI = (
            f"sqlite:///{os.path.join(BASE_DIR, 'zeronexus.db')}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Keep database connections healthy on Vercel
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # -------------------------------------------------
    # Cloudinary Configuration
    # -------------------------------------------------
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # -------------------------------------------------
    # Mail Configuration
    # -------------------------------------------------
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER",
        MAIL_USERNAME,
    )

    # -------------------------------------------------
    # Upload Configuration
    # -------------------------------------------------
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "app",
        "static",
        "uploads",
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

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

    # -------------------------------------------------
    # Security Settings
    # -------------------------------------------------
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        os.getenv("SESSION_COOKIE_SECURE", "False") == "True"
    )

    REMEMBER_COOKIE_SECURE = (
        os.getenv("REMEMBER_COOKIE_SECURE", "False") == "True"
    )

    WTF_CSRF_TIME_LIMIT = None

    # -------------------------------------------------
    # Admin Settings
    # -------------------------------------------------
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    # -------------------------------------------------
    # Public Site URL
    # -------------------------------------------------
    SITE_URL = os.getenv(
        "SITE_URL",
        "http://127.0.0.1:5000",
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False

    # Force secure cookies in production
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}