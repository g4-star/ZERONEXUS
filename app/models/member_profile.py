from app.extensions import db
import secrets


class MemberProfile(db.Model):

    __tablename__ = 'member_profiles'


    # -------------------------------------------------
    # Primary Key
    # -------------------------------------------------
    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # -------------------------------------------------
    # Basic Information
    # -------------------------------------------------
    full_name = db.Column(
        db.String(120),
        nullable=False
    )

    role = db.Column(
        db.String(120)
    )

    bio = db.Column(
        db.Text
    )


    # -------------------------------------------------
    # Profile Photo
    # -------------------------------------------------
    photo = db.Column(
        db.String(255),
        default='img/placeholders/member_placeholder.jpg'
    )


    # -------------------------------------------------
    # Professional Links
    # -------------------------------------------------
    linkedin_url = db.Column(
        db.String(255)
    )

    github_url = db.Column(
        db.String(255)
    )

    portfolio_url = db.Column(
        db.String(255)
    )


    # -------------------------------------------------
    # Contact Information
    # -------------------------------------------------
    email = db.Column(
        db.String(120)
    )

    whatsapp_number = db.Column(
        db.String(50)
    )


    # -------------------------------------------------
    # Skills
    # -------------------------------------------------
    skills = db.Column(
        db.Text
    )


    # -------------------------------------------------
    # Secure Profile Token
    # -------------------------------------------------
    profile_token = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
        default=lambda: secrets.token_hex(32)
    )


    # -------------------------------------------------
    # Team Relationship
    # -------------------------------------------------
    team_id = db.Column(
        db.Integer,
        db.ForeignKey('teams.id'),
        nullable=False
    )


    # -------------------------------------------------
    # User Account Connection
    # -------------------------------------------------
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        unique=True,
        nullable=True
    )


    user = db.relationship(
        "User",
        back_populates="member_profile"
    )


    # -------------------------------------------------
    # String Representation
    # -------------------------------------------------
    def __repr__(self):

        return f'<Member {self.full_name}>'