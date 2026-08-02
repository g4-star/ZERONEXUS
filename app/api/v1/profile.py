from flask import request, jsonify
from flask_login import login_required, current_user

from . import api
from app.services.profile_service import ProfileService


@api.route("/profile")
@login_required
def profile():

    return jsonify(

        ProfileService.get_profile(

            current_user

        )

    )


@api.route("/profile/update", methods=["POST"])
@login_required
def update_profile():

    data = request.get_json()

    ProfileService.update_profile(

        current_user,

        data

    )

    return jsonify(

        {

            "success": True,

            "message": "Profile updated."

        }

    )