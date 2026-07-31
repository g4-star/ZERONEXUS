from flask import render_template
from . import academy
from flask import request
from app.ai.tutor import ask_nexus_ai
from app.extensions import csrf


@academy.route("/")
def home():
    return render_template("academy/academy.html")


@academy.route("/python")
def python_course():
    return render_template("academy/course.html")


@academy.route("/python/module/<int:module_id>")
def python_module(module_id):

    lessons = {
        1: {
            "title": "What is Python?",
            "description": "Learn what Python is, where it is used, and why it is one of the world's most popular programming languages."
        },
        2: {
            "title": "Installing Python",
            "description": "Install Python and configure your coding environment."
        },
        3: {
            "title": "Variables",
            "description": "Understand variables and how to store information."
        },
        4: {
            "title": "Data Types",
            "description": "Learn strings, integers, floats and booleans."
        },
        5: {
            "title": "Conditions",
            "description": "Learn if, elif and else statements."
        },
        6: {
            "title": "Loops",
            "description": "Repeat code using for and while loops."
        },
        7: {
            "title": "Functions",
            "description": "Write reusable blocks of code using functions."
        },
        8: {
            "title": "Lists",
            "description": "Store multiple values using Python lists."
        },
        9: {
            "title": "Dictionaries",
            "description": "Work with key-value pairs."
        },
        10: {
            "title": "File Handling",
            "description": "Read and write files using Python."
        },
        11: {
            "title": "Object-Oriented Programming",
            "description": "Understand classes and objects."
        },
        12: {
            "title": "Final Project",
            "description": "Build a complete Python project."
        }
    }

    lesson = lessons.get(module_id)

    if lesson is None:
        return "Lesson Not Found", 404

    return render_template(
        "academy/module.html",
        lesson=lesson,
        module_id=module_id
    )


@csrf.exempt
@academy.route("/tutor", methods=["GET", "POST"])
def tutor():

    course = request.args.get("course", "Python")
    lesson = request.args.get("lesson", "General")

    answer = None

    if request.method == "POST":

        question = request.form.get("question")

        if question:
            answer = ask_nexus_ai(
                course,
                lesson,
                question
            )

    return render_template(
        "academy/tutor.html",
        answer=answer,
        course=course,
        lesson=lesson
    )