from django.db import models
import cloudinary
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator

cloudinary.config(
    cloud_name="dvjg6st2t",
    api_key="352511942345566",
    api_secret="JyGRhYmoWMZbE2r21GCwnCv4fyg"
)

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    duration_years = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.course_name

class Student(models.Model):
    enrollment_number = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20, default="abc@123")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    current_semester = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(12)]
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_photo = CloudinaryField("image", blank=True,default="cjkou0lq67se1odjzbrq")

    def __str__(self):
        return self.enrollment_number

class Subject(models.Model):
    subject_code = models.CharField(max_length=20, primary_key=True)
    subject_name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    credits = models.IntegerField(validators=[MinValueValidator(1)])
    SUB_CHOICES = [
        ('compulsory', "Compulsory"),
        ('elective', "Elective"),
        ('fbl', "FBL")
    ]
    subject_type = models.CharField(max_length=10, choices=SUB_CHOICES, default="compulsory")
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.subject_name} ({self.subject_code})"

class Faculty(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_photo = CloudinaryField('image', blank=True, default="cjkou0lq67se1odjzbrq")
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    subjects = models.ManyToManyField(Subject, through='FacultySubject')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class FacultySubject(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )

    class Meta:
        unique_together= ['faculty', 'subject']

    def __str__(self):
        return f"{self.faculty} - {self.subject}"