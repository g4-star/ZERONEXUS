from datetime import datetime

from app.extensions import db


class Announcement(db.Model):

    __tablename__ = "announcements"

    # ==========================================
    # Primary Key
    # ==========================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================
    # Content
    # ==========================================

    title = db.Column(
        db.String(150),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(30),
        default="General"
    )

    pinned = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ==========================================
    # Relationships
    # ==========================================

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    team = db.relationship(
        "Team",
        back_populates="announcements"
    )

    author = db.relationship(
        "User",
        back_populates="announcements"
    )

    def __repr__(self):

        return f"<Announcement {self.title}>"