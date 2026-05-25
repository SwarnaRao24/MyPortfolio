from django.contrib import admin
from django.utils.html import format_html
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
    list_display = (
        'status_badge',
        'full_name',
        'email',
        'phone_number',
        'selected_services',
        'submitted_at',
    )
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email', 'selected_services', 'message')
    readonly_fields = ('first_name', 'last_name', 'email', 'phone_number', 'selected_services', 'message',
                       'submitted_at')
    actions = ['mark_as_read', 'mark_as_unread']

    # Show a coloured NEW badge for unread bookings
    @admin.display(description='Status')
    def status_badge(self, obj):
        if not obj.is_read:
            return format_html(
                '<span style="background:#06b6d4;color:#000;padding:2px 10px;'
                'font-weight:900;font-size:11px;letter-spacing:0.1em;'
                'text-transform:uppercase;">NEW</span>'
            )
        return format_html(
            '<span style="color:#6b7280;font-size:11px;text-transform:uppercase;">Read</span>'
        )

    @admin.display(description='Name')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    # Auto-mark as read when admin opens the detail view
    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=['is_read'])
        return super().change_view(request, object_id, form_url, extra_context)

    @admin.action(description='Mark selected bookings as read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} booking(s) marked as read.')

    @admin.action(description='Mark selected bookings as unread')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} booking(s) marked as unread.')

    # Sort unread bookings to the top by default
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('is_read', '-submitted_at')