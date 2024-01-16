from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ..views import TaskViewSets

app_name = 'task'

router = DefaultRouter()
router.register('', TaskViewSets)

urlpatterns = [
    path('', include(router.urls)),
]
