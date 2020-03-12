from django.contrib import admin

# Register your models here.
from .models import Student
from .models import Professor
from .models import Module
from .models import Teaching
from .models import Rating

class StudentAdmin(admin.ModelAdmin):
    # display field
    list_display = ('student_id', 'student_name', 'student_email', 'student_password')
    # which field can go to edit
    list_display_links = ('student_id', 'student_name', 'student_email')

admin.site.register(Student,StudentAdmin)

class ProfessorAdmin(admin.ModelAdmin):
    # display field
    list_display = ('professor_id', 'professor_name', 'professor_email', 'professor_password')
    # which field can go to edit
    list_display_links = ('professor_id', 'professor_name', 'professor_email')

admin.site.register(Professor,ProfessorAdmin)

class ModuleAdmin(admin.ModelAdmin):
    # display field
    list_display = ('module_code', 'module_name')
    # which field can go to edit
    list_display_links = ('module_code', 'module_name')

admin.site.register(Module,ModuleAdmin)

class TeachingAdmin(admin.ModelAdmin):
    # display field
    list_display = ('teaching_id', 'module_code', 'professor_id', 'academic_year','academic_semester')
    # which field can go to edit
    list_display_links = ('teaching_id', 'module_code', 'professor_id', 'academic_year','academic_semester')

admin.site.register(Teaching,TeachingAdmin)

class RatingAdmin(admin.ModelAdmin):
    # display field
    list_display = ('rating_id', 'teaching_id', 'student_id', 'rating')
    # which field can go to edit
    list_display_links = ('rating_id', 'teaching_id', 'student_id', 'rating')

admin.site.register(Rating,RatingAdmin)