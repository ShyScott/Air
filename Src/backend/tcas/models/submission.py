from django.db import models

from .course import Course


class Submission(models.Model):
    title = models.CharField(max_length=128)
    percentage = models.IntegerField()

    course = models.ForeignKey(
        Course,
        models.CASCADE,
        related_name='submissions',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title
