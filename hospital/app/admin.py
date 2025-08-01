from django.contrib import admin
from .models import Patient, Staff, Department, Appointment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'bed_number', 'assigned_doctor', 'discharge_status')
    list_filter = ('assigned_doctor',)
    search_fields = ('name', 'bed_number')
    actions = ['mark_discharged']

    def discharge_status(self, obj):
        return obj.is_discharged
    discharge_status.boolean = True
    discharge_status.short_description = 'Discharged'

    def mark_discharged(self, request, queryset):
        queryset.update(is_discharged=True)
    mark_discharged.short_description = "Mark selected patients as discharged"

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'phone')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'department', 'appointment_date', 'appointment_time', 'get_status')
    list_filter = ('department', 'doctor', 'status')  # Now status is a real field
    search_fields = ('patient__name', 'doctor__user__first_name')
    date_hierarchy = 'appointment_date'

    def get_status(self, obj):
        return obj.status
    get_status.short_description = 'Status'