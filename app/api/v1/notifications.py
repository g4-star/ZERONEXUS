from flask import jsonify
from flask_login import login_required, current_user

from . import api
from app.services.notification_service import NotificationService


@api.route("/notifications")
@login_required
def notifications():

    notifications = NotificationService.unread(

        current_user

    )

    data = []

    for notification in notifications:

        data.append({

            "title":

                getattr(

                    notification,

                    "title",

                    ""

                ),

            "message":

                getattr(

                    notification,

                    "message",

                    ""

                )

        })

    return jsonify(data)