from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import (
    Length,
    Optional,
    URL
)


class EditProfileForm(FlaskForm):

    # ==========================================
    # Profile Photo
    # ==========================================

    profile_image = FileField(
        "Profile Picture",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Images only!"
            )
        ]
    )

    # ==========================================
    # Basic Information
    # ==========================================

    full_name = StringField(
        "Full Name",
        validators=[
            Optional(),
            Length(max=120)
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

    location = StringField(
        "Location",
        validators=[
            Optional(),
            Length(max=120)
        ]
    )

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

    skills = TextAreaField(
        "Skills",
        validators=[
            Optional(),
            Length(max=500)
        ]
    )

    # ==========================================
    # Professional Links
    # ==========================================

    portfolio = StringField(
        "Portfolio",
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

    # ==========================================
    # Submit
    # ==========================================

    submit = SubmitField(
        "Save Changes"
    )