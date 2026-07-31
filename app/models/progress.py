from app.extensions import db


class UserProgress(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    lesson_id = db.Column(
        db.Integer,
        nullable=False
    )

    completed = db.Column(
        db.Boolean,
        default=False
    )