from app.extensions import db


class Team(db.Model):

    __tablename__ = "teams"

    # =====================================================
    # Basic Information
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    slug = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    short_description = db.Column(
        db.String(255)
    )

    description = db.Column(
        db.Text
    )

    # =====================================================
    # Team Administrator
    # =====================================================

    team_admin_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    team_admin = db.relationship(
        "User",
        foreign_keys=[team_admin_id],
        uselist=False
    )

    # =====================================================
    # Public Team Lead Information
    # =====================================================

    lead_name = db.Column(
        db.String(120)
    )

    lead_role = db.Column(
        db.String(120)
    )

    lead_image = db.Column(
        db.String(255),
        default="img/placeholders/team_lead_placeholder.jpg"
    )

    banner_image = db.Column(
        db.String(255),
        default="img/placeholders/team_banner_placeholder.jpg"
    )

    # =====================================================
    # Team Members
    # =====================================================

    members = db.relationship(
        "MemberProfile",
        backref="team",
        lazy=True,
        cascade="all, delete-orphan"
    )

    users = db.relationship(
        "User",
        back_populates="team",
        foreign_keys="User.team_id",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # =====================================================
    # Team Projects
    # =====================================================

    projects = db.relationship(
        "Project",
        back_populates="team",
        lazy=True,
        cascade="all, delete-orphan"
    )

    # =====================================================
    # Meetings
    # =====================================================

    meetings = db.relationship(
        "Meeting",
        back_populates="team",
        cascade="all, delete-orphan",
    )

    # =====================================================
    # Announcements
    # =====================================================

    announcements = db.relationship(
        "Announcement",
        back_populates="team",
        cascade="all, delete-orphan",
        lazy=True
    )

    # =====================================================
    # Team Chat Channels
    # =====================================================

    channels = db.relationship(
        "ChatChannel",
        back_populates="team",
        cascade="all, delete-orphan",
        lazy=True
    )

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self):
        return f"<Team {self.name}>"