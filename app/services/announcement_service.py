from app.models.announcement import Announcement


class AnnouncementService:
    @staticmethod
    def latest(limit=10):
        return (
            Announcement.query
            .order_by(
                Announcement.pinned.desc(),
                Announcement.created_at.desc()
            )
            .limit(limit)
            .all()
        )