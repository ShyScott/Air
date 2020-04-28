from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=128, unique=True)
    duration = models.DateField(auto_now_add=True)
    form_method = models.SmallIntegerField(null=True)
    member_count_primary = models.IntegerField(default=0)
    team_count_primary = models.IntegerField(default=0)
    member_count_secondary = models.IntegerField(default=0)
    team_count_secondary = models.IntegerField(default=0)
    floating_band = models.FloatField(default=0)

    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        related_name='courses_teach',
        null=True,
        blank=True,
    )

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='courses_in',
        blank=True,
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
