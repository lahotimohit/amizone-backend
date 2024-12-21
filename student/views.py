from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.db.models import Count
from django.http import JsonResponse
from . import models
from timetable import models as tt

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
    def post(self, request):
        try:
            enrollment = request.data["enrollment"]
            student = models.Student.objects.get(enrollment_number=enrollment)
            subjects = models.Subject.objects.filter(
                course=student.course, 
                semester=student.current_semester
            )

            subject_data = []
            
            for subject in subjects:
                subject_info = {
                    'subject_code': subject.subject_code,
                    'subject_name': subject.subject_name,
                    'course': subject.course.course_name,
                    'semester': subject.semester,
                    'credits': subject.credits,
                    'subject_type': subject.get_subject_type_display(),
                    'description': subject.description,
                }

                attendance_counts = tt.Attendance.objects.filter(
                    student=student,
                    subject=subject
                ).values('status').annotate(count=Count('status'))
                
                attendance_info = {
                    'present': 0,
                    'absent': 0,
                    'late': 0
                }
                
                for item in attendance_counts:
                    attendance_info[item['status']] = item['count']
                
                total_classes = sum(attendance_info.values())
                attendance_percentage = 0
                if total_classes > 0:
                    attendance_percentage = round(
                        (attendance_info['present'] + attendance_info['late']) * 100 / total_classes, 
                        2
                    )
                
                subject_info['attendance'] = {
                    'present': attendance_info['present'],
                    'absent': attendance_info['absent'],
                    'late': attendance_info['late'],
                    'total_classes': total_classes,
                    'attendance_percentage': attendance_percentage
                }
                
                subject_data.append(subject_info)
            
            return Response({
                "status": "success",
                "student_name": f"{student.first_name} {student.last_name}",
                "enrollment": student.enrollment_number,
                "course": student.course.course_name,
                "semester": student.current_semester,
                "student_subjects": subject_data
            }, status=status.HTTP_200_OK)
            
        except models.Student.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Student not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        except KeyError:
            return Response({
                "status": "error",
                "message": "Enrollment number is required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class StudentsSubFaculties(APIView):
    def post(self,request):
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
                
                # Modified to include both faculty name and profile photo
                faculty_info = [{
                    'name': fs.faculty.__str__(),
                    'profile_photo': request.build_absolute_uri(fs.faculty.profile_photo.url) if fs.faculty.profile_photo else None
                } for fs in faculty_subjects]
                
                subject_faculty_list.append({
                    'subject_code': subject.subject_code,
                    'subject_name': subject.subject_name,
                    'faculty': faculty_info
                })
            
            return Response({
                "status": "success",
                "data": {
                    "student_name": f"{student.first_name} {student.last_name}",
                    "course": student.course.course_name,
                    "semester": student.current_semester,
                    "subjects": subject_faculty_list
                }
            }, status=status.HTTP_200_OK)

        except models.Student.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Student not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)