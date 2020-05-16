from django.db import models
from django.conf import settings


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        related_name='student_profile',
        primary_key=True,
    )
    student_id = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    gpa = models.FloatField(null=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.student_id
