from django.contrib import admin
from .models import Experience, Project, Service, ContactMessage

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'location', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'company_name')
    search_fields = ('job_title', 'company_name', 'summary')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'tech_stack', 'associated_experience', 'created_at')
    list_filter = ('associated_experience', 'created_at')
    search_fields = ('title', 'description', 'tech_stack')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'price', 'active')
    list_filter = ('service_type', 'active')
    search_fields = ('title', 'description')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Updated to match your new split-name and multi-service schema fields
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('first_name', 'last_name', 'email', 'selected_services', 'message')