from datetime import datetime

from app.extensions import db
from app.models.presence import UserPresence


class PresenceService:

    @staticmethod
    def user_connected(user, socket_id):

        presence = UserPresence.query.filter_by(
            user_id=user.id
        ).first()

        if not presence:

            presence = UserPresence(
                user_id=user.id
            )

            db.session.add(presence)

        presence.online = True
        presence.socket_id = socket_id
        presence.last_seen = datetime.utcnow()

        db.session.commit()

        return presence

    @staticmethod
    def user_disconnected(user):

        presence = UserPresence.query.filter_by(
            user_id=user.id
        ).first()

        if not presence:
            return

        presence.online = False
        presence.socket_id = None
        presence.last_seen = datetime.utcnow()

        db.session.commit()

    @staticmethod
    def online_members(team):

        online = []

        for user in team.users:

            presence = UserPresence.query.filter_by(
                user_id=user.id,
                online=True
            ).first()

            if presence:
                online.append(user)

        return online