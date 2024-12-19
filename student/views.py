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
        subjects = models.Subject.objects.filter(course=student.course, semester=student.current_semester)
        subject_list = list(subjects.values())
        return Response({"student_subjects": subject_list}, status=status.HTTP_200_OK)
    
class StudentsSubFaculties(APIView):
    def get(self,request):
        enrollment = request.data["enrollment"]
        try:
            student = models.Student.objects.get(enrollment_number=enrollment)
            subjects = models.Subject.objects.filter(
                course=student.course,
                semester=student.current_semester
            ).select_related('course')

            subject_faculty_list = []
            for subject in subjects:
                faculty_subjects = models.FacultySubject.objects.filter(
                    subject=subject,
                    semester=student.current_semester
                ).select_related('faculty', 'subject')
                
                faculty_names = [fs.faculty.__str__() for fs in faculty_subjects]
                
                subject_faculty_list.append({
                    'subject_code': subject.subject_code,
                    'subject_name': subject.subject_name,
                    'subject_type': subject.get_subject_type_display(),
                    'credits': subject.credits,
                    'faculty': faculty_names
                })
            
            return Response({
                'status': True,
                'message': 'Subjects retrieved successfully',
                'data': {
                    'student_name': f"{student.first_name} {student.last_name}",
                    'course': student.course.course_name,
                    'semester': student.current_semester,
                    'subjects': subject_faculty_list
                }
            })
        
        except models.Student.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Student not found',
                'data': None
            })
        except Exception as e:
            return Response({
                'status': False,
                'message': str(e),
                'data': None
            })
