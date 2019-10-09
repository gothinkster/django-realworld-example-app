from __future__ import unicode_literals


def has_permission(user, proposal, speaker=False, reviewer=False):
    """
    Returns whether or not ther user has permission to review this proposal,
    with the specified requirements.

    If ``speaker`` is ``True`` then the user can be one of the speakers for the
    proposal.  If ``reviewer`` is ``True`` the speaker can be a part of the
    reviewer group.
    """
    if user.is_superuser:
        return True
    if speaker:
        if user == proposal.speaker.user or \
           proposal.additional_speakers.filter(user=user).exists():
            return True
    if reviewer:
        if user.groups.filter(name="reviewers").exists():
            return True
    return False
