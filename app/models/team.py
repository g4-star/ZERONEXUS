from app.extensions import db


class Team(db.Model):

    __tablename__ = 'teams'


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
    
    meetings = db.relationship(
        "Meeting",
        back_populates="team",
        cascade="all, delete-orphan",
        lazy=True
    )

    announcements = db.relationship(
        "Announcement",
        back_populates="team",
        cascade="all, delete-orphan",
        lazy=True
    )


    # =====================================
    # Legacy Public Team Lead Information
    # (Keeps your current website working)
    # =====================================

    lead_name = db.Column(
        db.String(120)
    )


    lead_role = db.Column(
        db.String(120)
    )


    lead_image = db.Column(
        db.String(255),
        default='img/placeholders/team_lead_placeholder.jpg'
    )


    banner_image = db.Column(
        db.String(255),
        default='img/placeholders/team_banner_placeholder.jpg'
    )



    # =====================================
    # Public Profiles
    # Existing ZeroNexus members
    # =====================================

    members = db.relationship(
        'MemberProfile',
        backref='team',
        lazy=True,
        cascade='all, delete-orphan'
    )



    # =====================================
    # User Accounts
    # New Authentication System
    # =====================================

    members = db.relationship(
        'MemberProfile',
        backref='team',
        lazy=True,
        cascade='all, delete-orphan'
    )


    users = db.relationship(
        "User",
        back_populates="team",
        lazy=True,
        cascade="all, delete-orphan"
    )


    # =====================================
    # Team Projects
    # =====================================

    projects = db.relationship(
        "Project",
        back_populates="team",
        lazy=True,
        cascade="all, delete-orphan"
    )



    def __repr__(self):

        return f'<Team {self.name}>'