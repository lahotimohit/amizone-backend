from student import models as st
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

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

class AttendanceSummary(models.Model):
    student = models.ForeignKey(st.Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(st.Subject, on_delete=models.CASCADE)
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    total_classes = models.IntegerField(default=0)
    classes_attended = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'subject', 'semester']

    @property
    def attendance_percentage(self):
        if self.total_classes == 0:
            return 0
        return round((self.classes_attended * 100.0) / self.total_classes, 2)

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.semester})"