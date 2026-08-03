from app.extensions import db
from app.models.notification import Notification


class NotificationService:

    # =====================================================
    # Create Notification
    # =====================================================

    @staticmethod
    def create(
        user,
        title,
        message,
        notification_type,
        link=None
    ):

        notification = Notification(
            user_id=user.id,
            title=title,
            message=message,
            type=notification_type,
            link=link
        )

        db.session.add(notification)
        db.session.commit()

        return notification

    # =====================================================
    # Notify Entire Team
    # =====================================================

    @staticmethod
    def notify_team(
        team,
        title,
        message,
        notification_type,
        link=None
    ):

        notifications = []

        for member in team.users:

            notification = Notification(
                user_id=member.id,
                title=title,
                message=message,
                type=notification_type,
                link=link
            )

            db.session.add(notification)
            notifications.append(notification)

        db.session.commit()

        return notifications

    # =====================================================
    # Mark Notification Read
    # =====================================================

    @staticmethod
    def mark_read(notification):

        notification.is_read = True

        db.session.commit()

    # =====================================================
    # Mark All Read
    # =====================================================

    @staticmethod
    def mark_all_read(user):

        Notification.query.filter_by(
            user_id=user.id,
            is_read=False
        ).update(
            {"is_read": True}
        )

        db.session.commit()

    # =====================================================
    # Unread Count
    # =====================================================

    @staticmethod
    def unread_count(user):

        return Notification.query.filter_by(
            user_id=user.id,
            is_read=False
        ).count()

    # =====================================================
    # User Notifications
    # =====================================================

    @staticmethod
    def get_notifications(user):

        return Notification.query.filter_by(
            user_id=user.id
        ).order_by(
            Notification.created_at.desc()
        ).all()