from datetime import datetime

from app.extensions import db


class TeamProject(db.Model):

    __tablename__ = "team_projects"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    title = db.Column(
        db.String(200),
        nullable=False
    )


    description = db.Column(
        db.Text,
        nullable=False
    )


    status = db.Column(
        db.String(50),
        default="Planning",
        nullable=False
    )


    priority = db.Column(
        db.String(20),
        default="Medium",
        nullable=False
    )


    deadline = db.Column(
        db.Date,
        nullable=True
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )


    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )


    team = db.relationship(
        "Team",
        backref=db.backref(
            "projects",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )


    creator = db.relationship(
        "User",
        backref="created_projects"
    )
