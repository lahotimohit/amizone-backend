from django.urls import path
from . import views

urlpatterns = [
    path("api/login", views.StudentLogin.as_view()),
    path('api/get-all-subjects', views.StudentSubjects.as_view()),
    path('api/get-all-faculties', views.StudentsSubFaculties.as_view())
]
