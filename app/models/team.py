from app.extensions import db

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)

    slug = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)

    short_description = db.Column(db.String(255))
    description = db.Column(db.Text)

    lead_name = db.Column(db.String(120))
    lead_role = db.Column(db.String(120))

    lead_image = db.Column(
        db.String(255),
        default='img/placeholders/team_lead_placeholder.jpg'
    )

    banner_image = db.Column(
        db.String(255),
        default='img/placeholders/team_banner_placeholder.jpg'
    )

    members = db.relationship(
        'MemberProfile',
        backref='team',
        lazy=True,
        cascade='all, delete-orphan'
    )

    projects = db.relationship(
        'Project',
        backref='team',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Team {self.name}>'