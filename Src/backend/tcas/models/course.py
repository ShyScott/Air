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

    @property
    def team_nums(self):
        team_nums = [self.member_count_primary for _ in range(self.team_count_primary)]
        team_nums.extend([self.member_count_secondary for _ in range(self.team_count_secondary)])
        return team_nums

    def clear_forming_options(self):
        self.form_method = None
        self.member_count_primary = self.member_count_secondary = self.team_count_primary = self.team_count_secondary = 0
        self.save()
