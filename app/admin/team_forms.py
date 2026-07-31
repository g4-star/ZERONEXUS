from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class EditTeamForm(FlaskForm):
    name = StringField('Team Name', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    lead_name = StringField('Lead Name')
    lead_role = StringField('Lead Role')
    short_description = TextAreaField('Short Description')
    description = TextAreaField('Full Description')

    submit = SubmitField('Save Changes')