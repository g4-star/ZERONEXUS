from datetime import datetime
import secrets

from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db


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
    # User Role
    # admin
    # team_lead
    # member
    # =====================================================

    role = db.Column(
        db.String(50),
        default="member",
        nullable=False
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
        nullable=False,
        default=lambda: secrets.token_urlsafe(50)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # Relationships
    # =====================================================

    team = db.relationship(
        "Team",
        back_populates="users"
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

    # Announcements created by this user
    announcements = db.relationship(
        "Announcement",
        back_populates="author",
        lazy=True
    )

    # =====================================================
    # Password Helpers
    # =====================================================

    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )

    # =====================================================
    # String Representation
    # =====================================================

    def __repr__(self):

        return f"<User {self.username}>"