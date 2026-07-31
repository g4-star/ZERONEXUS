from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Optional, URL, Email


class MemberProfileForm(FlaskForm):
    full_name = StringField('Full Name')
    role = StringField('Role')
    bio = TextAreaField('Bio')

    linkedin_url = StringField(
        'LinkedIn URL',
        validators=[Optional(), URL()]
    )

    github_url = StringField(
        'GitHub URL',
        validators=[Optional(), URL()]
    )

    portfolio_url = StringField(
        'Portfolio URL',
        validators=[Optional(), URL()]
    )

    email = StringField(
        'Email',
        validators=[Optional(), Email()]
    )

    whatsapp_number = StringField('WhatsApp Number')

    skills = TextAreaField('Skills')

    submit = SubmitField('Save Changes')
