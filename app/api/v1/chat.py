from flask import jsonify
from flask_login import login_required, current_user

from . import api
from app.services.chat_service import ChatService


@api.route("/chat")
@login_required
def chat():

    team = getattr(

        current_user,

        "team",

        None

    )

    team_id = team.id if team else None

    messages = ChatService.latest(

        team_id

    )

    data = []

    for msg in messages:

        data.append({

            "message":

                getattr(

                    msg,

                    "message",

                    ""

                ),

            "user_id":

                getattr(

                    msg,

                    "user_id",

                    None

                )

        })

    return jsonify(data)