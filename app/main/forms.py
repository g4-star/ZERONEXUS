from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Optional, URL, Email


class MemberProfileForm(FlaskForm):
    # -------------------------------------------------
    # Basic Information
    # -------------------------------------------------
    full_name = StringField('Full Name')
    role = StringField('Role')
    bio = TextAreaField('Bio')

    # -------------------------------------------------
    # Profile Picture Upload
    # -------------------------------------------------
    photo = FileField(
        'Profile Picture',
        validators=[
            FileAllowed(
                ['jpg', 'jpeg', 'png', 'webp', 'gif'],
                'Images only!'
            )
        ]
    )

    # -------------------------------------------------
    # Professional Links
    # -------------------------------------------------
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

    # -------------------------------------------------
    # Contact Information
    # -------------------------------------------------
    email = StringField(
        'Email',
        validators=[Optional(), Email()]
    )

    whatsapp_number = StringField('WhatsApp Number')

    # -------------------------------------------------
    # Skills
    # -------------------------------------------------
    skills = TextAreaField('Skills')

    # -------------------------------------------------
    # Submit Button
    # -------------------------------------------------
    submit = SubmitField('Save Changes')