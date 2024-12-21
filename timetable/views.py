from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from student.models import Student, Subject
from . import models
from django.db.models import Q

class ClassesByDay(APIView):
    def post(self, request):
        day = request.data["day"]
        enrollment = request.data['enrollment']
        student = Student.objects.get(enrollment_number=enrollment)
        try:
            day = day.capitalize()
            classes = models.TimeTable.objects.filter(
                day_of_week=day, semester=student.current_semester
            ).select_related(
                'subject', 
                'faculty', 
                'course'
            ).order_by('start_time')

            timetable_data = []
            for class_obj in classes:
                timetable_data.append({
                    'subject': class_obj.subject.subject_name,
                    'faculty': str(class_obj.faculty),
                    'start_time': class_obj.start_time.strftime('%I:%M %p'),
                    'end_time': class_obj.end_time.strftime('%I:%M %p'),
                    'room_number': class_obj.room_number,
                    'semester': class_obj.semester,
                    'course': str(class_obj.course)
                })

            return Response({
                'day': day,
                'classes': timetable_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StudentAttendanceData(APIView):
    def post(self, request):
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