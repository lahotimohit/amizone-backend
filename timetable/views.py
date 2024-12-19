from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from student.models import Student, Subject
from . import models
from django.db.models import Q


class StudentAttendanceData(APIView):
    def get(self, request):
        enrollment = request.data['enrollment']
        try:
            student = Student.objects.get(enrollment_number=enrollment)
            subjects = Subject.objects.filter(
                course=student.course,
                semester=student.current_semester
            )
            
            attendance_data = []
            
            for subject in subjects:
                attendance_counts = models.Attendance.objects.filter(
                    student=student,
                    subject=subject
                ).values('status').annotate(count=Count('status'))
                
                status_counts = {
                    'present': 0,
                    'absent': 0,
                    'late': 0
                }
                
                for item in attendance_counts:
                    status_counts[item['status']] = item['count']
                
                attendance_entry = {
                    'subject_name': subject.subject_name,
                    'present': status_counts['present'],
                    'absent': status_counts['absent'],
                    'late': status_counts['late']
                }
                
                attendance_data.append(attendance_entry)
            
            return Response({
                'status': True,
                'message': 'Attendance data retrieved successfully',
                'data': attendance_data
            })
            
        except Student.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Student not found',
                'data': []
            })
        except Exception as e:
            return Response({
                'status': False,
                'message': str(e),
                'data': []
            })