from flask import jsonify
from flask_login import login_required, current_user

from . import api
from app.services.project_service import ProjectService


@api.route("/projects")
@login_required
def projects():

    projects = ProjectService.user_projects(

        current_user

    )

    result = []

    for project in projects:

        result.append({

            "id": project.id,

            "title": getattr(project, "title", ""),

            "status": getattr(project, "status", ""),

            "completion":

                ProjectService.completion(

                    project

                )

        })

    return jsonify(result)