from datetime import datetime


def format_datetime(value):

    if not value:

        return ""

    return value.strftime(

        "%d %b %Y %I:%M %p"

    )


def time_ago(value):

    if not value:

        return ""

    delta = datetime.utcnow() - value

    if delta.days > 0:

        return f"{delta.days} day(s) ago"

    hours = delta.seconds // 3600

    if hours > 0:

        return f"{hours} hour(s) ago"

    minutes = delta.seconds // 60

    if minutes > 0:

        return f"{minutes} minute(s) ago"

    return "Just now"


def percentage(part, whole):

    if whole == 0:

        return 0

    return round(

        (part / whole) * 100

    )