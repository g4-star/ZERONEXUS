from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    BooleanField,
    SubmitField
)
from wtforms.validators import DataRequired, Length


class CreateAnnouncementForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[
            DataRequired(message="Title is required."),
            Length(max=150)
        ]
    )

    content = TextAreaField(
        "Content",
        validators=[
            DataRequired(message="Content is required.")
        ]
    )

    category = SelectField(
        "Category",
        choices=[
            ("General", "General"),
            ("Announcement", "Announcement"),
            ("Meeting", "Meeting"),
            ("Event", "Event"),
            ("Important", "Important"),
            ("Update", "Update"),
        ],
        default="General"
    )

    pinned = BooleanField("Pin this announcement")

    submit = SubmitField("Post Announcement")