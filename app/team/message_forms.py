from flask_wtf import FlaskForm

from wtforms import (
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length
)


class MessageForm(FlaskForm):

    message = TextAreaField(

        "Message",

        validators=[

            DataRequired(),

            Length(max=3000)

        ]

    )

    submit = SubmitField("Send")