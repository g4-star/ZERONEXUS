from datetime import datetime

from app.extensions import db


class Project(db.Model):

    __tablename__ = "projects"


    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # =====================================================
    # BASIC INFORMATION
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
        db.String(255),
        nullable=True
    )


    demo_url = db.Column(
        db.String(255),
        nullable=True
    )


    # =====================================================
    # PROJECT FILE UPLOAD
    # =====================================================

    project_file = db.Column(
        db.String(500),
        nullable=True
    )


    file_name = db.Column(
        db.String(255),
        nullable=True
    )


    file_size = db.Column(
        db.String(50),
        nullable=True
    )


    # =====================================================
    # ACCESS CONTROL
    # =====================================================

    # team  -> only assigned team members
    # all   -> every team can access

    visibility = db.Column(
        db.String(30),
        default="team",
        nullable=False
    )


    # =====================================================
    # PROJECT STATUS
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
        db.Date,
        nullable=True
    )


    # =====================================================
    # TIMESTAMPS
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
    # OWNERSHIP
    # =====================================================

    # NULL means global admin project

    team_id = db.Column(
        db.Integer,
        db.ForeignKey("teams.id"),
        nullable=True
    )


    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )


    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    team = db.relationship(
        "Team",
        back_populates="projects"
    )


    creator = db.relationship(
        "User",
        back_populates="projects"
    )


    # =====================================================
    # HELPERS
    # =====================================================

    def is_global(self):

        return self.visibility == "all"


    def is_team_project(self):

        return self.visibility == "team"


    def __repr__(self):

        return f"<Project {self.title}>"