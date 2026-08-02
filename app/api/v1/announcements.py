from flask import jsonify
from flask_login import login_required

from . import api
from app.services.announcement_service import AnnouncementService


@api.route("/announcements")
@login_required
def announcements():

    announcements = AnnouncementService.latest()

    result = []

    for item in announcements:

        result.append({

            "id": item.id,

            "title": getattr(item, "title", ""),

            "body": getattr(item, "content", "")

        })

    return jsonify(result)