from django.contrib import admin
from django.contrib.auth.models import User, Group
from . import models

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'duration_years')
    search_fields = ('course_name',)
    list_filter = ('duration_years',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_number', "first_name", "last_name", "course", "current_semester", "email")
    search_fields = ('enrollment_number', "first_name", "last_name", "email")
    list_filter = ('course', 'current_semester')

class FacultySubjectInline(admin.TabularInline):
    model = models.FacultySubject
    extra = 1

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'subject_name', 'course', 'semester', 'credits')
    search_fields = ('subject_code', 'subject_name')
    list_filter = ('course', 'semester', 'credits')

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'email', 'phone', 'status')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('status',)
    inlines = [FacultySubjectInline]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'

class FacultySubjectAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'subject', 'semester')
    search_fields = ('faculty__first_name', 'faculty__last_name', 
                    'subject__subject_name')
    list_filter = ('semester',)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Subject, SubjectAdmin)
admin.site.register(models.Faculty, FacultyAdmin)
admin.site.register(models.FacultySubject, FacultySubjectAdmin)