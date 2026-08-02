from datetime import datetime

try:
    from app.models.chat_message import ChatMessage
except ImportError:
    ChatMessage = None

from app.extensions import db


class ChatService:

    @staticmethod
    def latest(team_id=None, limit=50):

        if not ChatMessage:
            return []

        query = ChatMessage.query

        if team_id and hasattr(ChatMessage, "team_id"):

            query = query.filter_by(team_id=team_id)

        if hasattr(ChatMessage, "created_at"):

            query = query.order_by(
                ChatMessage.created_at.desc()
            )

        return query.limit(limit).all()

    @staticmethod
    def create(user, message, team_id=None):

        if not ChatMessage:

            return None

        data = {

            "message": message,

            "created_at": datetime.utcnow()

        }

        if hasattr(ChatMessage, "user_id"):

            data["user_id"] = user.id

        if team_id and hasattr(ChatMessage, "team_id"):

            data["team_id"] = team_id

        chat = ChatMessage(**data)

        db.session.add(chat)

        db.session.commit()

        return chat

    @staticmethod
    def delete(chat):

        db.session.delete(chat)

        db.session.commit()