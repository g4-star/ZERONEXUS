from app.extensions import db


class Quiz(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    lesson_id = db.Column(
        db.Integer,
        nullable=False
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    answer = db.Column(
        db.String(200)
    )