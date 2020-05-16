from rest_framework.pagination import PageNumberPagination

from django.db.models import Q
from django.contrib.auth.backends import ModelBackend, UserModel


class ExtendedPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 50


class UsernameEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        try:
            user = UserModel.objects.get(Q(username=username) | Q(student_profile__email=username))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
