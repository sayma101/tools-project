"""
Admin configuration for events app
"""
from django.contrib import admin
from .models import Event, Announcement, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for events"""
    list_display = ['title', 'event_type', 'start_date', 'location', 'organizer', 'is_featured', 'is_published']
    list_filter = ['event_type', 'is_featured', 'is_published', 'start_date', 'department']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-start_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'event_type', 'organizer', 'department')
        }),
        ('Date & Location', {
            'fields': ('start_date', 'end_date', 'location')
        }),
        ('Registration', {
            'fields': ('registration_required', 'registration_deadline', 'max_participants')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Media & Status', {
            'fields': ('image', 'is_featured', 'is_published')
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """Admin interface for announcements"""
    list_display = ['title', 'author', 'priority', 'target_audience', 'is_pinned', 'is_published', 'created_at']
    list_filter = ['priority', 'is_pinned', 'is_published', 'created_at', 'department']
    search_fields = ['title', 'content', 'target_audience']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-is_pinned', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content', 'author', 'department')
        }),
        ('Targeting & Priority', {
            'fields': ('target_audience', 'priority', 'expiry_date')
        }),
        ('Attachment & Status', {
            'fields': ('attachment', 'is_published', 'is_pinned')
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    """Admin interface for event registrations"""
    list_display = ['user', 'event', 'registration_date', 'is_confirmed']
    list_filter = ['is_confirmed', 'registration_date', 'event__event_type']
    search_fields = ['user__first_name', 'user__last_name', 'event__title']
    readonly_fields = ['registration_date']
    ordering = ['-registration_date']