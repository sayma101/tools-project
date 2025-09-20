"""
Accounts app models for user profiles and faculty
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Department(models.Model):
    """Model for university departments"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(
        'Faculty', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='headed_department'
    )
    established_year = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    """Extended profile for students"""
    YEAR_CHOICES = [
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
        ('graduate', 'Graduate'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    year = models.CharField(max_length=10, choices=YEAR_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/students/', blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"
    
    def get_absolute_url(self):
        return reverse('accounts:profile')

class Faculty(models.Model):
    """Model for faculty members"""
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('instructor', 'Instructor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    specialization = models.CharField(max_length=200)
    qualification = models.TextField()
    experience_years = models.IntegerField(default=0)
    phone = models.CharField(max_length=15, blank=True)
    office_room = models.CharField(max_length=20, blank=True)
    office_hours = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/faculty/', blank=True)
    bio = models.TextField(blank=True)
    research_interests = models.TextField(blank=True)
    publications = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    join_date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Faculty"
        ordering = ['user__last_name', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_designation_display()}"
    
    def get_absolute_url(self):
        return reverse('accounts:faculty_detail', kwargs={'pk': self.pk})