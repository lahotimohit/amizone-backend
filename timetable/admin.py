from django.contrib import admin
from .models import TimeTable, Attendance

@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'start_time', 'end_time', 'subject', 
                   'faculty', 'room_number', 'semester', 'course')
    list_filter = ('day_of_week', 'semester', 'course', 'faculty')
    search_fields = ('subject__subject_name', 'faculty__first_name', 
                    'faculty__last_name', 'room_number')
    ordering = ('day_of_week', 'start_time')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status', 'marked_by', 
                   'created_at')
    list_filter = ('status', 'date', 'subject', 'marked_by')
    search_fields = ('student__first_name', 'student__last_name', 
                    'subject__subject_name', 'marked_by__first_name', 
                    'marked_by__last_name')
    readonly_fields = ('created_at',)
    ordering = ('-date', '-created_at')
    
    date_hierarchy = 'date' 
    
    list_per_page = 50
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'student', 'subject', 'marked_by'
        )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "marked_by":
            kwargs["queryset"] = db_field.related_model.objects.filter(
                status='active'
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)