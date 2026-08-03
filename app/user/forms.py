from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import (
    StringField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    Optional,
    Length,
    URL
)


class EditProfileForm(FlaskForm):

    # =====================================================
    # Profile Picture
    # =====================================================

    profile_image = FileField(
        "Profile Picture",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only!"
            )
        ]
    )

    # =====================================================
    # Basic Information
    # =====================================================

    full_name = StringField(
        "Full Name",
        validators=[
            Optional(),
            Length(max=120)
        ]
    )

    username = StringField(
        "Username",
        validators=[
            Optional(),
            Length(min=3, max=50)
        ]
    )

    bio = TextAreaField(
        "Bio",
        validators=[
            Optional(),
            Length(max=1000)
        ]
    )

    phone = StringField(
        "Phone",
        validators=[
            Optional(),
            Length(max=40)
        ]
    )

    whatsapp = StringField(
        "WhatsApp",
        validators=[
            Optional(),
            Length(max=40)
        ]
    )

    location = StringField(
        "Location",
        validators=[
            Optional(),
            Length(max=120)
        ]
    )

    # =====================================================
    # Professional Information
    # =====================================================

    job_title = StringField(
        "Job Title",
        validators=[
            Optional(),
            Length(max=120)
        ]
    )

    company = StringField(
        "Company",
        validators=[
            Optional(),
            Length(max=120)
        ]
    )

    experience_level = StringField(
        "Experience Level",
        validators=[
            Optional(),
            Length(max=80)
        ]
    )

    favorite_language = StringField(
        "Favorite Programming Language",
        validators=[
            Optional(),
            Length(max=80)
        ]
    )

    skills = TextAreaField(
        "Skills",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )

    # =====================================================
    # Professional Links
    # =====================================================

    portfolio = StringField(
        "Portfolio Website",
        validators=[
            Optional(),
            URL()
        ]
    )

    github = StringField(
        "GitHub",
        validators=[
            Optional(),
            URL()
        ]
    )

    linkedin = StringField(
        "LinkedIn",
        validators=[
            Optional(),
            URL()
        ]
    )

    twitter = StringField(
        "Twitter / X",
        validators=[
            Optional(),
            URL()
        ]
    )

    # =====================================================
    # Cybersecurity Profiles
    # =====================================================

    tryhackme = StringField(
        "TryHackMe",
        validators=[
            Optional(),
            URL()
        ]
    )

    hackthebox = StringField(
        "Hack The Box",
        validators=[
            Optional(),
            URL()
        ]
    )

    ctftime = StringField(
        "CTFTime",
        validators=[
            Optional(),
            URL()
        ]
    )

    # =====================================================
    # Submit
    # =====================================================

    submit = SubmitField("Save Changes")