"""
Courses app views for course management and enrollment
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Count
from django.core.paginator import Paginator

from .models import Course, Enrollment, Assignment, Material
from accounts.models import Department, StudentProfile

class CourseListView(ListView):
    """List view for all courses"""
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True).select_related(
            'department', 'instructor__user'
        ).annotate(
            enrollment_count=Count('enrollments', filter=Q(enrollments__is_active=True))
        )
        
        # Filter by department
        department = self.request.GET.get('department')
        if department:
            queryset = queryset.filter(department__code=department)
        
        # Filter by level
        level = self.request.GET.get('level')
        if level:
            queryset = queryset.filter(level=level)
        
        # Filter by semester
        semester = self.request.GET.get('semester')
        if semester:
            queryset = queryset.filter(semester=semester)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(description__icontains=search) |
                Q(instructor__user__first_name__icontains=search) |
                Q(instructor__user__last_name__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['levels'] = Course.LEVEL_CHOICES
        context['semesters'] = Course.SEMESTER_CHOICES
        context['filters'] = {
            'department': self.request.GET.get('department', ''),
            'level': self.request.GET.get('level', ''),
            'semester': self.request.GET.get('semester', ''),
            'search': self.request.GET.get('search', ''),
        }
        return context

class CourseDetailView(DetailView):
    """Detail view for individual course"""
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Check if user is enrolled
        if self.request.user.is_authenticated:
            try:
                student_profile = StudentProfile.objects.get(user=self.request.user)
                context['is_enrolled'] = Enrollment.objects.filter(
                    student=student_profile,
                    course=course,
                    is_active=True
                ).exists()
            except StudentProfile.DoesNotExist:
                context['is_enrolled'] = False
        else:
            context['is_enrolled'] = False
        
        # Get course materials and assignments
        context['materials'] = course.materials.filter(is_published=True)
        context['assignments'] = course.assignments.filter(is_published=True)
        context['prerequisites'] = course.prerequisites.all()
        
        return context

class EnrollView(LoginRequiredMixin, TemplateView):
    """View for enrolling in a course"""
    
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk, is_active=True)
        
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            messages.error(request, 'Only students can enroll in courses.')
            return redirect('courses:course_detail', pk=pk)
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=student_profile, course=course, is_active=True).exists():
            messages.warning(request, 'You are already enrolled in this course.')
            return redirect('courses:course_detail', pk=pk)
        
        # Check if course is full
        if course.is_full:
            messages.error(request, 'This course is full.')
            return redirect('courses:course_detail', pk=pk)
        
        # Create enrollment
        Enrollment.objects.create(student=student_profile, course=course)
        messages.success(request, f'Successfully enrolled in {course.name}!')
        
        return redirect('courses:course_detail', pk=pk)

class UnenrollView(LoginRequiredMixin, TemplateView):
    """View for unenrolling from a course"""
    
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            enrollment = Enrollment.objects.get(
                student=student_profile,
                course=course,
                is_active=True
            )
            enrollment.is_active = False
            enrollment.status = 'dropped'
            enrollment.save()
            messages.success(request, f'Successfully unenrolled from {course.name}.')
        except (StudentProfile.DoesNotExist, Enrollment.DoesNotExist):
            messages.error(request, 'You are not enrolled in this course.')
        
        return redirect('courses:course_detail', pk=pk)

class MyCoursesView(LoginRequiredMixin, TemplateView):
    """View for student's enrolled courses"""
    template_name = 'courses/my_courses.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            student_profile = StudentProfile.objects.get(user=self.request.user)
            enrollments = Enrollment.objects.filter(
                student=student_profile,
                is_active=True
            ).select_related('course', 'course__instructor__user')
            
            context['enrollments'] = enrollments
        except StudentProfile.DoesNotExist:
            context['enrollments'] = []
        
        return context

class DepartmentListView(ListView):
    """List view for all departments"""
    model = Department
    template_name = 'courses/department_list.html'
    context_object_name = 'departments'
    
    def get_queryset(self):
        return Department.objects.annotate(
            course_count=Count('course', filter=Q(course__is_active=True))
        )

class DepartmentDetailView(DetailView):
    """Detail view for individual department"""
    model = Department
    template_name = 'courses/department_detail.html'
    context_object_name = 'department'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        department = self.get_object()
        
        context['courses'] = Course.objects.filter(
            department=department,
            is_active=True
        ).select_related('instructor__user')
        
        context['faculty'] = department.faculty_set.all().select_related('user')
        
        return context