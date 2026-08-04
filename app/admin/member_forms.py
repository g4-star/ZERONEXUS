from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, Email, Optional


class AddMemberForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    role = SelectField("Role", choices=[("member","Member"),("team_lead","Team Lead")], validators=[DataRequired()])

    team_id = SelectField(
        'Team / Group',
        coerce=int,
        validators=[DataRequired()]
    )

    email = StringField('Email', validators=[Optional(), Email()])
    whatsapp_number = StringField('WhatsApp Number', validators=[Optional()])

    linkedin_url = StringField('LinkedIn URL', validators=[Optional()])
    github_url = StringField('GitHub URL', validators=[Optional()])
    portfolio_url = StringField('Portfolio URL', validators=[Optional()])

    skills = TextAreaField('Skills')
    bio = TextAreaField('Bio')

    submit = SubmitField('Save Member')