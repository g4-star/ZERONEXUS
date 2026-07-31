from app.extensions import db
import secrets


class MemberProfile(db.Model):
    __tablename__ = 'member_profiles'

    # -------------------------------------------------
    # Primary Key
    # -------------------------------------------------
    id = db.Column(db.Integer, primary_key=True)

    # -------------------------------------------------
    # Basic Information
    # -------------------------------------------------
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120))
    bio = db.Column(db.Text)

    # -------------------------------------------------
    # Profile Photo
    # Default placeholder image
    # -------------------------------------------------
    photo = db.Column(
        db.String(255),
        default='img/placeholders/member_placeholder.jpg'
    )

    # -------------------------------------------------
    # Professional Links
    # -------------------------------------------------
    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(255))

    # -------------------------------------------------
    # Contact Information
    # -------------------------------------------------
    email = db.Column(db.String(120))
    whatsapp_number = db.Column(db.String(50))

    # -------------------------------------------------
    # Skills
    # -------------------------------------------------
    skills = db.Column(db.Text)

    # -------------------------------------------------
    # Secure Token
    # Used to generate a personal upload link such as:
    # /members/upload/<token>
    # -------------------------------------------------
    profile_token = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
        default=lambda: secrets.token_hex(32)
    )

    # -------------------------------------------------
    # Relationship to Team
    # -------------------------------------------------
    team_id = db.Column(
        db.Integer,
        db.ForeignKey('teams.id'),
        nullable=False
    )

    # -------------------------------------------------
    # String Representation
    # -------------------------------------------------
    def __repr__(self):
        return f'<Member {self.full_name}>'