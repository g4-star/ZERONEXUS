from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    DateField,
    TimeField,
    IntegerField,
    URLField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    URL,
    NumberRange
)


class MeetingForm(FlaskForm):

    title = StringField(
        "Meeting Title",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    description = TextAreaField(
        "Description",
        validators=[
            DataRequired()
        ]
    )

    meeting_date = DateField(
        "Meeting Date",
        validators=[
            DataRequired()
        ]
    )

    meeting_time = TimeField(
        "Meeting Time",
        validators=[
            DataRequired()
        ]
    )

    duration = IntegerField(
        "Duration (Minutes)",
        default=60,
        validators=[
            NumberRange(
                min=5,
                max=600
            )
        ]
    )

    meet_link = URLField(
        "Google Meet Link",
        validators=[
            DataRequired(),
            URL()
        ]
    )

    submit = SubmitField(
        "Save Meeting"
    )