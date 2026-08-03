from datetime import datetime

from app.extensions import db


class Notification(db.Model):

    __tablename__ = "notifications"

    # =====================================================
    # Primary Key
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # Receiver
    # =====================================================

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # =====================================================
    # Notification Details
    # =====================================================

    title = db.Column(
        db.String(255),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    type = db.Column(
        db.String(50),
        nullable=False
    )

    link = db.Column(
        db.String(255),
        nullable=True
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    # =====================================================
    # Timestamps
    # =====================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =====================================================
    # Relationships
    # =====================================================

    user = db.relationship(
        "User",
        back_populates="notifications"
    )

    def __repr__(self):

        return f"<Notification {self.title}>"