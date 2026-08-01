from datetime import datetime

from app.extensions import db


class Project(db.Model):
    __tablename__ = "projects"

    # =====================================================
    # Primary Key
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # Basic Information
    # =====================================================

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    image = db.Column(
        db.String(255),
        default="img/placeholders/project_placeholder.jpg"
    )

    github_url = db.Column(
        db.String(255)
    )

    demo_url = db.Column(
        db.String(255)
    )

    # =====================================================
    # Project Workflow
    # =====================================================

    status = db.Column(
        db.String(30),
        default="Planning",
        nullable=False
    )

    priority = db.Column(
        db.String(20),
        default="Medium",
        nullable=False
    )

    progress = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    deadline = db.Column(
        db.Date
    )

    # =====================================================
    # Ownership
    # =====================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # =====================================================
    # Relationships
    # =====================================================

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=False
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    team = db.relationship(
        "Team",
        back_populates="projects"
    )

    creator = db.relationship(
        "User",
        back_populates="projects"
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):

        return f"<Project {self.title}>"