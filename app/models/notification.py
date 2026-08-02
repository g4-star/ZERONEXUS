from datetime import datetime

from app.extensions import db


class Notification(db.Model):

    __tablename__ = "notifications"

    id = db.Column(

        db.Integer,

        primary_key=True

    )

    title = db.Column(

        db.String(200),

        nullable=False

    )

    message = db.Column(

        db.Text,

        nullable=False

    )

    is_read = db.Column(

        db.Boolean,

        default=False

    )

    created_at = db.Column(

        db.DateTime,

        default=datetime.utcnow

    )

    user_id = db.Column(

        db.Integer,

        db.ForeignKey("users.id")

    )

    def mark_read(self):

        self.is_read = True

    def __repr__(self):

        return f"<Notification {self.title}>"