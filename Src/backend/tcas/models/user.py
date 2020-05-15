from django.contrib.auth.models import AbstractUser

from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnStoragePlaceholderImage


class User(AbstractUser):
    avatar = VersatileImageField(
        upload_to='avatars',
        blank=True,
        placeholder_image=OnStoragePlaceholderImage('default_avatar.jpg')
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        if not self.is_teacher:
            return '%s (%s)' % (self.username, self.student_profile.student_id)
        return self.username

    @property
    def is_teacher(self):
        return not hasattr(self, 'student_profile')
