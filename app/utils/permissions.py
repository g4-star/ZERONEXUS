from functools import wraps

from flask import (
    abort
)

from flask_login import (
    current_user
)


# =====================================================
# ROLE CHECKS
# =====================================================

def is_super_admin():

    return (
        current_user.is_authenticated
        and current_user.role == "super_admin"
    )


def is_team_admin():

    return (
        current_user.is_authenticated
        and current_user.role == "team_admin"
    )


def is_team_lead():

    return (
        current_user.is_authenticated
        and current_user.role == "team_lead"
    )


def is_member():

    return (
        current_user.is_authenticated
        and current_user.role == "member"
    )


# =====================================================
# DECORATORS
# =====================================================

def super_admin_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if not is_super_admin():

            abort(403)

        return view(*args, **kwargs)

    return wrapped


def team_admin_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if not (
            is_super_admin()
            or
            is_team_admin()
        ):

            abort(403)

        return view(*args, **kwargs)

    return wrapped


def team_lead_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if not (
            is_super_admin()
            or
            is_team_admin()
            or
            is_team_lead()
        ):

            abort(403)

        return view(*args, **kwargs)

    return wrapped


def member_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if not current_user.is_authenticated:

            abort(403)

        return view(*args, **kwargs)

    return wrapped