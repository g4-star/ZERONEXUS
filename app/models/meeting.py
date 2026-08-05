from datetime import datetime

from app.extensions import db


class Meeting(db.Model):
    __tablename__ = "meetings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    meeting_date = db.Column(
        db.Date,
        nullable=False
    )

    meeting_time = db.Column(
        db.Time,
        nullable=False
    )

    duration = db.Column(
        db.Integer,
        default=60
    )

    meet_link = db.Column(
        db.String(500),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Scheduled"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    # Relationships
    creator = db.relationship(
        "User",
        backref="meetings_created"
    )

    team = db.relationship(
        "Team",
        back_populates="meetings"
    )

    def __repr__(self):
        return f"<Meeting {self.title}>"