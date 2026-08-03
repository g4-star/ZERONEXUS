from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    
    __tablename__ = "users"

    # =====================================================
    # Primary Key
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # Login Information
    # =====================================================

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    # =====================================================
    # User Roles
    # =====================================================

    role = db.Column(
        db.String(50),
        nullable=False,
        default="member"
    )

    # =====================================================
    # Team Assignment
    # =====================================================

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=True
    )

    # =====================================================
    # Account Status
    # =====================================================

    must_change_password = db.Column(
        db.Boolean,
        default=True
    )

    is_active = db.Column(
        db.Boolean,
        default=False
    )

    activation_token = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # Profile Information
    # =====================================================

    profile_image = db.Column(
        db.String(255),
        nullable=True
    )

    full_name = db.Column(
        db.String(120),
        nullable=True
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    phone = db.Column(
        db.String(30),
        nullable=True
    )

    whatsapp = db.Column(
        db.String(30),
        nullable=True
    )

    location = db.Column(
        db.String(120),
        nullable=True
    )

    # =====================================================
    # Professional Information
    # =====================================================

    job_title = db.Column(
        db.String(120),
        nullable=True
    )

    company = db.Column(
        db.String(120),
        nullable=True
    )

    experience_level = db.Column(
        db.String(80),
        nullable=True
    )

    favorite_language = db.Column(
        db.String(80),
        nullable=True
    )

    skills = db.Column(
        db.Text,
        nullable=True
    )

    # =====================================================
    # Social Links
    # =====================================================

    portfolio = db.Column(
        db.String(255),
        nullable=True
    )

    github = db.Column(
        db.String(255),
        nullable=True
    )

    linkedin = db.Column(
        db.String(255),
        nullable=True
    )

    twitter = db.Column(
        db.String(255),
        nullable=True
    )

    # =====================================================
    # Cybersecurity Profiles
    # =====================================================

    tryhackme = db.Column(
        db.String(255),
        nullable=True
    )

    hackthebox = db.Column(
        db.String(255),
        nullable=True
    )

    ctftime = db.Column(
        db.String(255),
        nullable=True
    )

    # =====================================================
    # Relationships
    # =====================================================

    team = db.relationship(
        "Team",
        back_populates="users",
        foreign_keys=[team_id]
    )

    member_profile = db.relationship(
        "MemberProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    projects = db.relationship(
        "Project",
        back_populates="creator",
        lazy=True
    )

    announcements = db.relationship(
        "Announcement",
        back_populates="author",
        lazy=True
    )

    # =====================================================
    # Team Chat
    # =====================================================

    sent_messages = db.relationship(
        "ChatMessage",
        foreign_keys="ChatMessage.sender_id",
        back_populates="sender",
        lazy=True
    )

    created_channels = db.relationship(
        "ChatChannel",
        foreign_keys="ChatChannel.created_by",
        back_populates="creator",
        lazy=True
    )

    # =====================================================
    # Notifications
    # =====================================================

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

    # =====================================================
    # Password Helpers
    # =====================================================

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self):
        return f"<User {self.username}>"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))