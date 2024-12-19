from django.urls import path
from . import views

urlpatterns = [
    path("api/attendance", views.StudentAttendanceData.as_view()),
    path("api/get-classes-by-day", views.ClassesByDay.as_view())
]
