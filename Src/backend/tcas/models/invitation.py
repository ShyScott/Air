from django.db import models
from django.conf import settings

from .team import Team


class Invitation(models.Model):
    team = models.ForeignKey(
        Team,
        models.CASCADE,
        related_name='invitations',
    )
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='+',
    )
    invitee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='+',
    )
    invite_time = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField()
