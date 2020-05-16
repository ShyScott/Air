from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, _, UnicodeUsernameValidator

from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnStoragePlaceholderImage


class EnglishUsernameValidator(RegexValidator):
    regex = r'^[\w.@+\- ]+\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_/space characters.'
    )
    flags = 0


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_/space only.'),
        validators=[EnglishUsernameValidator()],
    )
    email = models.EmailField(
        _('email address'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    avatar = VersatileImageField(
        upload_to='avatars',
        blank=True,
        placeholder_image=OnStoragePlaceholderImage('default_avatar.jpg')
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']

    def __str__(self):
        if not self.is_teacher:
            return '%s (%s)' % (self.username, self.student_profile.student_id)
        return self.username

    @property
    def is_teacher(self):
        return not hasattr(self, 'student_profile')
