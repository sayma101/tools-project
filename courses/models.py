"""
Courses app models for course management
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Department, Faculty, StudentProfile

class Course(models.Model):
    """Model for university courses"""
    SEMESTER_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
    ]
    
    LEVEL_CHOICES = [
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('postgraduate', 'Postgraduate'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    credits = models.IntegerField()
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    year = models.IntegerField()
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    max_students = models.IntegerField(default=50)
    schedule = models.CharField(max_length=200, help_text="e.g., Mon/Wed/Fri 10:00-11:00")
    classroom = models.CharField(max_length=50, blank=True)
    syllabus = models.FileField(upload_to='courses/syllabi/', blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['department', 'code']
        unique_together = ['code', 'semester', 'year']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'pk': self.pk})
    
    @property
    def enrolled_count(self):
        return self.enrollments.filter(is_active=True).count()
    
    @property
    def available_spots(self):
        return self.max_students - self.enrolled_count
    
    @property
    def is_full(self):
        return self.enrolled_count >= self.max_students

class Enrollment(models.Model):
    """Model for student course enrollments"""
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('failed', 'Failed'),
    ]
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='enrolled')
    grade = models.CharField(max_length=5, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.code}"

class Assignment(models.Model):
    """Model for course assignments"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_points = models.IntegerField(default=100)
    attachment = models.FileField(upload_to='assignments/', blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"

class Material(models.Model):
    """Model for course materials"""
    MATERIAL_TYPES = [
        ('lecture', 'Lecture Notes'),
        ('reading', 'Reading Material'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    file = models.FileField(upload_to='course_materials/', blank=True)
    url = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"