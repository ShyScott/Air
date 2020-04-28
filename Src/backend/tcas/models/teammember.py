from django.db import models
from django.conf import settings

from .submission import Submission
from .contribution import Contribution


class TeamMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    team = models.ForeignKey('Team', models.CASCADE)
    vote = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        related_name='+',
        null=True,
        blank=True,
    )
    leader_bonus = models.SmallIntegerField(default=0)

    contributions = models.ManyToManyField(
        Submission,
        related_name='+',
        blank=True,
        through=Contribution,
    )

    class Meta:
        unique_together = ('user', 'team')
