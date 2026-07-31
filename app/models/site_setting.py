from app.extensions import db


class SiteSetting(db.Model):
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)

    site_name = db.Column(db.String(120), default='ZeroNexus')
    contact_email = db.Column(db.String(120))
    whatsapp_number = db.Column(db.String(50))
    footer_text = db.Column(
        db.String(255),
        default='© ZeroNexus. All rights reserved.'
    )

    theme_name = db.Column(db.String(50), default='cyber-blue')
    mode = db.Column(db.String(10), default='dark')

    hero_title = db.Column(
        db.String(255),
        default='ZeroNexus Cybersecurity Hub'
    )

    hero_subtitle = db.Column(
        db.Text,
        default='Explore our cybersecurity teams, projects, and member portfolios.'
    )

    linkedin_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))
    twitter_url = db.Column(db.String(255))

    def __repr__(self):
        return f'<SiteSetting {self.site_name}>'