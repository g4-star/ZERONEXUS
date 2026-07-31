from app.extensions import db

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    github_url = db.Column(db.String(255))
    demo_url = db.Column(db.String(255))

    image = db.Column(
        db.String(255),
        default='img/placeholders/project_placeholder.jpg'
    )

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    def __repr__(self):
        return f'<Project {self.title}>'