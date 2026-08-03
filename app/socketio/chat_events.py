from flask_login import current_user
from flask_socketio import (
    emit,
    join_room,
    leave_room
)

from app.extensions import socketio
from app.models.chat import ChatChannel
from app.services.chat_service import ChatService
from flask import request
from app.services.presence_service import PresenceService


# =====================================================
# CONNECT
# =====================================================

@socketio.on("connect")
def connect():

    if not current_user.is_authenticated:
        return False

    PresenceService.user_connected(
        current_user,
        request.sid
    )

    emit(
        "presence_update",
        {
            "user_id": current_user.id,
            "username": current_user.username,
            "online": True
        },
        broadcast=True
    )


# =====================================================
# DISCONNECT
# =====================================================

@socketio.on("disconnect")
def disconnect():

    if current_user.is_authenticated:

        PresenceService.user_disconnected(
            current_user
        )

        emit(
            "presence_update",
            {
                "user_id": current_user.id,
                "username": current_user.username,
                "online": False
            },
            broadcast=True
        )


# =====================================================
# JOIN CHANNEL
# =====================================================

@socketio.on("join_channel")
def join_channel(data):

    channel_id = data.get("channel_id")

    channel = ChatChannel.query.get(channel_id)

    if not channel:
        return

    if channel.team_id != current_user.team_id:
        return

    room = f"channel_{channel.id}"

    join_room(room)

    emit(
        "joined_channel",
        {
            "channel_id": channel.id
        }
    )


# =====================================================
# LEAVE CHANNEL
# =====================================================

@socketio.on("leave_channel")
def leave_channel(data):

    channel_id = data.get("channel_id")

    room = f"channel_{channel_id}"

    leave_room(room)


# =====================================================
# SEND MESSAGE
# =====================================================

@socketio.on("send_message")
def send_message(data):

    channel = ChatChannel.query.get(
        data.get("channel_id")
    )

    if not channel:
        return

    if channel.team_id != current_user.team_id:
        return

    message = ChatService.send_message(
        channel,
        current_user,
        data.get("content")
    )

    emit(
        "new_message",
        {
            "id": message.id,
            "sender": current_user.username,
            "sender_id": current_user.id,
            "content": message.content,
            "created_at": message.created_at.strftime("%H:%M")
        },
        room=f"channel_{channel.id}"
    )


# =====================================================
# USER TYPING
# =====================================================

@socketio.on("typing")
def typing(data):

    emit(
        "user_typing",
        {
            "user": current_user.username
        },
        room=f"channel_{data.get('channel_id')}",
        include_self=False
    )


# =====================================================
# STOP TYPING
# =====================================================

@socketio.on("stop_typing")
def stop_typing(data):

    emit(
        "user_stop_typing",
        {
            "user": current_user.username
        },
        room=f"channel_{data.get('channel_id')}",
        include_self=False
    )