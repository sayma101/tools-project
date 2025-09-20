"""
Admin configuration for main app
"""
from django.contrib import admin
from .models import ContactMessage, GalleryImage, GalleryVideo, UniversityInfo

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for contact messages"""
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Admin interface for gallery images"""
    list_display = ['title', 'uploaded_at', 'is_featured']
    list_filter = ['is_featured', 'uploaded_at']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_at']

@admin.register(GalleryVideo)
class GalleryVideoAdmin(admin.ModelAdmin):
    """Admin interface for gallery videos"""
    list_display = ['title', 'uploaded_at', 'is_featured']
    list_filter = ['is_featured', 'uploaded_at']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_at']

@admin.register(UniversityInfo)
class UniversityInfoAdmin(admin.ModelAdmin):
    """Admin interface for university information"""
    list_display = ['name', 'established_year', 'total_students', 'total_faculty']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not UniversityInfo.objects.exists()