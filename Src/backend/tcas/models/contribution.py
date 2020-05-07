from django.db import models

from .submission import Submission


class Contribution(models.Model):
    submission = models.ForeignKey(Submission, models.CASCADE)
    team_member = models.ForeignKey('TeamMember', models.CASCADE)

    """
    # level - The contribution level
    # 0 - None (0)
    # 1 - Little (0.33)
    # 2 - Fair (0.67)
    # 3 - Full (1)
    """
    level = models.SmallIntegerField()
    levels = {
        0: 0,
        1: 0.33,
        2: 0.67,
        3: 1,
    }

    class Meta:
        unique_together = ('submission', 'team_member')
