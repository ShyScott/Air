from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        ordering = ['id']

    def __str__(self):
        if not self.is_teacher:
            return '%s (%s)' % (self.username, self.student_profile.student_id)
        return self.username

    @property
    def is_teacher(self):
        return not hasattr(self, 'student_profile')
