from django.contrib import admin
from .models import Patient, Staff, Department

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'bed_number', 'assigned_doctor', 'is_discharged')
    list_filter = ('is_discharged', 'assigned_doctor')
    search_fields = ('name', 'bed_number')
    actions = ['mark_discharged']

    def mark_discharged(self, request, queryset):
        queryset.update(is_discharged=True)
    mark_discharged.short_description = "Mark selected patients as discharged"

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department')
    list_filter = ('role', 'department')

admin.site.register(Department)