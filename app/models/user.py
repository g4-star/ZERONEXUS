from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # LOGIN
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
    # ROLE
    # =====================================================

    role = db.Column(
        db.String(50),
        nullable=False,
        default="member"
    )

    # =====================================================
    # TEAM
    # =====================================================

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=True
    )

    # =====================================================
    # ACCOUNT
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
    # PROFILE
    # =====================================================

    profile_image = db.Column(
        db.String(255)
    )

    full_name = db.Column(
        db.String(120)
    )

    bio = db.Column(
        db.Text
    )

    phone = db.Column(
        db.String(30)
    )

    whatsapp = db.Column(
        db.String(30)
    )

    location = db.Column(
        db.String(120)
    )

    # =====================================================
    # PROFESSIONAL
    # =====================================================

    job_title = db.Column(
        db.String(120)
    )

    company = db.Column(
        db.String(120)
    )

    experience_level = db.Column(
        db.String(80)
    )

    favorite_language = db.Column(
        db.String(80)
    )

    skills = db.Column(
        db.Text
    )

    # =====================================================
    # SOCIAL
    # =====================================================

    portfolio = db.Column(
        db.String(255)
    )

    github = db.Column(
        db.String(255)
    )

    linkedin = db.Column(
        db.String(255)
    )

    twitter = db.Column(
        db.String(255)
    )

    # =====================================================
    # CYBERSECURITY
    # =====================================================

    tryhackme = db.Column(
        db.String(255)
    )

    hackthebox = db.Column(
        db.String(255)
    )

    ctftime = db.Column(
        db.String(255)
    )

    # =====================================================
    # RELATIONSHIPS
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

    meetings_created = db.relationship(
        "Meeting",
        back_populates="creator",
        lazy=True
    )

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

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
    # PASSWORD
    # =====================================================

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    # =====================================================
    # ROLE HELPERS
    # =====================================================

    @property
    def is_super_admin(self):
        return self.role == "super_admin"

    @property
    def is_team_lead(self):
        return self.role in (
            "super_admin",
            "team_lead",
            "Team Lead"
        )

    @property
    def is_member(self):
        return self.role in (
            "member",
            "Member"
        )

    @property
    def is_admin(self):
        return self.is_super_admin

    @property
    def display_name(self):
        return self.full_name or self.username

    # =====================================================
    # FLASK-LOGIN HELPERS
    # =====================================================

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self):
        return (
            f"<User id={self.id} "
            f"username='{self.username}' "
            f"role='{self.role}'>"
        )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))