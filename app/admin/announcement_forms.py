from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    BooleanField,
    SubmitField
)
from wtforms.validators import DataRequired, Length

from app.models import Team


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

    team_id = SelectField(
        "Target Team",
        coerce=int,
        validators=[
            DataRequired(message="Please select a team.")
        ]
    )

    pinned = BooleanField(
        "Pin this announcement"
    )

    submit = SubmitField(
        "Post Announcement"
    )

    def __init__(self, *args, **kwargs):

        # Remove the custom argument before calling FlaskForm
        teams = kwargs.pop("teams", None)

        super().__init__(*args, **kwargs)

        # Load every team if none was supplied
        if teams is None:
            teams = Team.query.order_by(
                Team.name.asc()
            ).all()

        # Build dropdown
        self.team_id.choices = [
            (-1, "🌍 All Teams")
        ]

        for team in teams:
            self.team_id.choices.append(
                (team.id, team.name)
            )