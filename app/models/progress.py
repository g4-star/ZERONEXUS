from datetime import datetime

from app.extensions import db


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    lesson_id = db.Column(
        db.Integer,
        db.ForeignKey("lessons.id"),
        nullable=False
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )

    completed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    last_accessed = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )