from datetime import datetime

from app.extensions import db


class ChatMessage(db.Model):

    __tablename__ = "chat_messages"

    id = db.Column(

        db.Integer,

        primary_key=True

    )

    message = db.Column(

        db.Text,

        nullable=False

    )

    created_at = db.Column(

        db.DateTime,

        default=datetime.utcnow

    )

    user_id = db.Column(

        db.Integer,

        db.ForeignKey("users.id"),

        nullable=False

    )

    team_id = db.Column(

        db.Integer,

        db.ForeignKey("teams.id"),

        nullable=True

    )

    def __repr__(self):

        return f"<ChatMessage {self.id}>"