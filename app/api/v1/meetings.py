from flask import jsonify
from flask_login import login_required

from . import api
from app.services.meeting_service import MeetingService


@api.route("/meetings")
@login_required
def meetings():

    meetings = MeetingService.upcoming()

    result = []

    for meeting in meetings:

        result.append({

            "id": meeting.id,

            "title": getattr(meeting, "title", ""),

            "date": str(

                getattr(

                    meeting,

                    "meeting_date",

                    ""

                )

            )

        })

    return jsonify(result)