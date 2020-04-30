from django.db import models
from django.conf import settings

from .course import Course
from .teammember import TeamMember


class Team(models.Model):
    name = models.CharField(max_length=256)
    is_generated = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    course = models.ForeignKey(
        Course,
        models.CASCADE,
        related_name='teams',
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='teams',
        blank=True,
        through=TeamMember,
        through_fields=('team', 'user'),
    )

    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        related_name='+',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
