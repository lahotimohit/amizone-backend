from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse
from . import models

class StudentLogin(APIView):
    def post(self, request):
        print(request.data)
        enrollment = request.data["enrollment"]
        password = request.data["password"]
        try:
            student = models.Student.objects.filter(Q(enrollment_number=enrollment) & Q(password=password)).exists()
            print(student, type(student))
            if student:
                return Response({"message": "Student credentials correct"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid Student"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"message": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentSubjects(APIView):
    def get(self,request):
        enrollment = request.data["enrollment"]
        student = models.Student.objects.get(enrollment_number=enrollment)
        course = student.course
        semester = student.current_semester
        subjects = models.Subject.objects.filter(course=course, semester=semester)
        subject_list = list(subjects.values())
        return Response({"student_subjects": subject_list}, status=status.HTTP_200_OK)