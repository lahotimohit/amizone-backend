from student import models as st
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Attendance(models.Model):
    student = models.ForeignKey(st.Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(st.Subject, on_delete=models.CASCADE)
    date = models.DateField()
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(st.Faculty, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class TimeTable(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday')
    ]
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(st.Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(st.Faculty, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    course = models.ForeignKey(st.Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['day_of_week', 'start_time', 'room_number']

    def __str__(self):
        return f"{self.subject} - {self.day_of_week} ({self.start_time})"