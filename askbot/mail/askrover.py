"""Email notifications for the Rover Q&A Community."""

from askbot import const


def process_instant_notifications(
    post,
    exclude_list=None,
    activity_type=None
):
    """Determine which notifications need to be sent and to whom for the
    given post and activity type.
    """
    # If this is an upvote.
    if activity_type == const.TYPE_ACTIVITY_VOTE_UP:
        pass

    # If this is a new answer.
    elif activity_type == const.TYPE_ACTIVITY_ANSWER:
        pass

    # If this is a comment on a question.
    elif activity_type == const.TYPE_ACTIVITY_COMMENT_QUESTION:
        pass

    # If this is a comment on an answer.
    elif activity_type == const.TYPE_ACTIVITY_COMMENT_ANSWER:
        pass


def send_instant_notifications(
    template=None,
    recipients=None,
):
    """Send instant notifications to the given recipients."""
