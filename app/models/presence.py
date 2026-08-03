from datetime import datetime

from app.extensions import db


class UserPresence(db.Model):

    __tablename__ = "user_presence"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    online = db.Column(
        db.Boolean,
        default=False
    )

    socket_id = db.Column(
        db.String(255)
    )

    last_seen = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User"
    )