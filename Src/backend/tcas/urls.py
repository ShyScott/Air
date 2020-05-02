from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('courses', views.CourseViewSet, basename='course')
router.register('submissions', views.SubmissionViewSet)
router.register('teams', views.TeamViewSet)
router.register('invitations', views.InvitationViewSet, basename='invitation')

urlpatterns = [
    path('', include(router.urls))
]
