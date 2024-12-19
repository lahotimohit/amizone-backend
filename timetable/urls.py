from django.urls import path
from . import views

urlpatterns = [
    path("api/attendance", views.StudentAttendanceData.as_view())
]
