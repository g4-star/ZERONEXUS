try:
    from app.models.notification import Notification
except ImportError:
    Notification = None

from app.extensions import db


class NotificationService:

    @staticmethod
    def unread(user):

        if not Notification:

            return []

        query = Notification.query

        if hasattr(Notification, "user_id"):

            query = query.filter_by(
                user_id=user.id
            )

        if hasattr(Notification, "is_read"):

            query = query.filter_by(
                is_read=False
            )

        return query.all()

    @staticmethod
    def count(user):

        return len(

            NotificationService.unread(user)

        )

    @staticmethod
    def create(user, title, message):

        if not Notification:

            return None

        data = {

            "title": title,

            "message": message

        }

        if hasattr(Notification, "user_id"):

            data["user_id"] = user.id

        notification = Notification(**data)

        db.session.add(notification)

        db.session.commit()

        return notification

    @staticmethod
    def mark_all_read(user):

        if not Notification:

            return

        notifications = Notification.query.filter_by(

            user_id=user.id,

            is_read=False

        ).all()

        for item in notifications:

            item.is_read = True

        db.session.commit()