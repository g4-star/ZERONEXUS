from datetime import datetime

from app.extensions import db
from app.models.chat import (
    ChatChannel,
    ChatMessage,
    MessageRead
)


class ChatService:

    # =====================================================
    # CHANNELS
    # =====================================================

    @staticmethod
    def create_channel(team, creator, name, description=""):

        channel = ChatChannel(
            team_id=team.id,
            created_by=creator.id,
            name=name,
            description=description
        )

        db.session.add(channel)
        db.session.commit()

        return channel

    @staticmethod
    def get_team_channels(team_id):

        return ChatChannel.query.filter_by(
            team_id=team_id
        ).order_by(ChatChannel.name.asc()).all()

    # =====================================================
    # MESSAGES
    # =====================================================

    @staticmethod
    def send_message(channel, sender, content):

        message = ChatMessage(
            channel_id=channel.id,
            sender_id=sender.id,
            content=content
        )

        db.session.add(message)
        db.session.commit()

        return message

    @staticmethod
    def get_messages(channel_id, limit=100):

        return ChatMessage.query.filter_by(
            channel_id=channel_id
        ).order_by(ChatMessage.created_at.asc()).limit(limit).all()

    @staticmethod
    def edit_message(message, new_content):

        message.content = new_content
        message.edited = True
        message.updated_at = datetime.utcnow()

        db.session.commit()

        return message

    @staticmethod
    def delete_message(message):

        message.deleted = True

        db.session.commit()

        return message

    # =====================================================
    # READ RECEIPTS
    # =====================================================

    @staticmethod
    def mark_as_read(message, user):

        exists = MessageRead.query.filter_by(
            message_id=message.id,
            user_id=user.id
        ).first()

        if exists:
            return exists

        read = MessageRead(
            message_id=message.id,
            user_id=user.id
        )

        db.session.add(read)
        db.session.commit()

        return read

    # =====================================================
    # HELPERS
    # =====================================================

    @staticmethod
    def unread_count(user, channel):

        return ChatMessage.query.filter(
            ChatMessage.channel_id == channel.id,
            ~ChatMessage.reads.any(
                MessageRead.user_id == user.id
            )
        ).count()