from datetime import datetime

from app.extensions import db


class TeamMessage(db.Model):

    __tablename__ = "team_messages"

    # ==========================================
    # Primary Key
    # ==========================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ==========================================
    # Message
    # ==========================================

    message = db.Column(
        db.Text,
        nullable=False
    )

    attachment = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    edited_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # ==========================================
    # Relationships
    # ==========================================

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    team = db.relationship(
        "Team",
        backref=db.backref(
            "messages",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    author = db.relationship(
        "User",
        backref=db.backref(
            "messages",
            lazy=True
        )
    )

    def __repr__(self):

        return f"<TeamMessage {self.id}>"