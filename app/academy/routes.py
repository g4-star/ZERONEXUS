from flask import render_template
from . import academy


@academy.route("/")
def home():

    return render_template(
        "academy/academy.html"
    )


@academy.route("/python")
def python_course():

    return render_template(
        "academy/course.html"
    )


@academy.route("/tutor")
def tutor():

    return render_template(
        "academy/tutor.html"
    )