from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from app.models.chat import ChatChannel, ChatMessage
from app.services.chat_service import ChatService

chat_api = Blueprint("chat_api", __name__, url_prefix="/api/chat")


# =====================================================
# GET TEAM CHANNELS
# =====================================================

@chat_api.route("/channels", methods=["GET"])
@login_required
def channels():

    if not current_user.team_id:
        return jsonify({
            "success": False,
            "message": "You are not assigned to a team."
        }), 403

    channels = ChatService.get_team_channels(current_user.team_id)

    return jsonify({
        "success": True,
        "channels": [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description
            }
            for c in channels
        ]
    })


# =====================================================
# GET CHANNEL MESSAGES
# =====================================================

@chat_api.route("/messages/<int:channel_id>", methods=["GET"])
@login_required
def messages(channel_id):

    channel = ChatChannel.query.get_or_404(channel_id)

    if channel.team_id != current_user.team_id:
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403

    messages = ChatService.get_messages(channel_id)

    return jsonify({
        "success": True,
        "messages": [
            {
                "id": m.id,
                "sender": m.sender.username,
                "sender_id": m.sender.id,
                "content": m.content,
                "edited": m.edited,
                "created_at": m.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for m in messages
            if not m.deleted
        ]
    })


# =====================================================
# SEND MESSAGE
# =====================================================

@chat_api.route("/send", methods=["POST"])
@login_required
def send():

    data = request.get_json()

    channel = ChatChannel.query.get_or_404(
        data["channel_id"]
    )

    if channel.team_id != current_user.team_id:
        return jsonify({
            "success": False,
            "message": "Access denied."
        }), 403

    message = ChatService.send_message(
        channel,
        current_user,
        data["content"]
    )

    return jsonify({
        "success": True,
        "message": {
            "id": message.id,
            "sender": current_user.username,
            "content": message.content,
            "created_at": message.created_at.strftime("%H:%M")
        }
    })