from datetime import datetime

from app.extensions import db


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(120), nullable=False, index=True)

    subject = db.Column(db.String(200), nullable=False)

    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    is_replied = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    ip_address = db.Column(
        db.String(45),
        nullable=True
    )

    user_agent = db.Column(
        db.Text,
        nullable=True
    )

    def __repr__(self):
        return (
            f"<ContactMessage "
            f"{self.full_name} "
            f"{self.email}>"
        )