from flask import jsonify, request
from flask_login import login_required

from . import api
from app.services.ai_service import AIService


@api.route("/ai/prompts")
@login_required
def prompts():

    return jsonify(

        AIService.starter_prompts()

    )


@api.route("/ai/chat", methods=["POST"])
@login_required
def ai_chat():

    data = request.get_json()

    prompt = data.get(

        "prompt",

        ""

    )

    response = AIService.generate(

        prompt

    )

    return jsonify(response)