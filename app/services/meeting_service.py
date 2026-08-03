from datetime import date

from app.models.meeting import Meeting


class MeetingService:
    @staticmethod
    def upcoming(limit=10):
        return (
            Meeting.query
            .filter(Meeting.meeting_date >= date.today())
            .order_by(
                Meeting.meeting_date.asc(),
                Meeting.meeting_time.asc()
            )
            .limit(limit)
            .all()
        )