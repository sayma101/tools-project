"""
Main app models for university website
"""
from django.db import models
from django.contrib.auth.models import User

class ContactMessage(models.Model):
    """Model for storing contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class GalleryImage(models.Model):
    """Model for gallery images"""
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/images/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title

class GalleryVideo(models.Model):
    """Model for gallery videos"""
    title = models.CharField(max_length=200)
    video_url = models.URLField(help_text="YouTube or Vimeo URL")
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title

class UniversityInfo(models.Model):
    """Model for storing university information"""
    name = models.CharField(max_length=200, default="International Islamic University Chittagong")
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    established_year = models.IntegerField()
    total_students = models.IntegerField(default=0)
    total_faculty = models.IntegerField(default=0)
    total_programs = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "University Information"
        verbose_name_plural = "University Information"
    
    def __str__(self):
        return self.name