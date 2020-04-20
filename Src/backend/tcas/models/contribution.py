from django.db import models

from .submission import Submission


class Contribution(models.Model):
    submission = models.ForeignKey(Submission, models.CASCADE)
    team_member = models.ForeignKey('TeamMember', models.CASCADE)
    level = models.SmallIntegerField()

    class Meta:
        unique_together = ('submission', 'team_member')
