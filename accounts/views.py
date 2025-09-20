"""
Accounts app views for authentication and user management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.core.paginator import Paginator

from .models import StudentProfile, Faculty, Department
from .forms import StudentRegistrationForm, StudentProfileForm, UserUpdateForm

class CustomLoginView(LoginView):
    """Custom login view with enhanced styling"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return self.get_redirect_url() or '/'

class RegisterView(TemplateView):
    """Student registration view"""
    template_name = 'accounts/register.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StudentRegistrationForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to our university.')
            return redirect('main:home')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})

class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if user is a student or faculty
        try:
            context['student_profile'] = StudentProfile.objects.get(user=self.request.user)
        except StudentProfile.DoesNotExist:
            context['student_profile'] = None
        
        try:
            context['faculty_profile'] = Faculty.objects.get(user=self.request.user)
        except Faculty.DoesNotExist:
            context['faculty_profile'] = None
            
        return context

class EditProfileView(LoginRequiredMixin, TemplateView):
    """Edit user profile view"""
    template_name = 'accounts/edit_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserUpdateForm(instance=self.request.user)
        
        try:
            student_profile = StudentProfile.objects.get(user=self.request.user)
            context['profile_form'] = StudentProfileForm(instance=student_profile)
        except StudentProfile.DoesNotExist:
            context['profile_form'] = None
            
        return context
    
    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            profile_form = StudentProfileForm(
                request.POST, 
                request.FILES, 
                instance=student_profile
            )
        except StudentProfile.DoesNotExist:
            profile_form = None
        
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {
                'user_form': user_form,
                'profile_form': profile_form
            })

class FacultyListView(ListView):
    """List view for all faculty members"""
    model = Faculty
    template_name = 'accounts/faculty_list.html'
    context_object_name = 'faculty_members'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Faculty.objects.select_related('user', 'department')
        
        # Filter by department if specified
        department = self.request.GET.get('department')
        if department:
            queryset = queryset.filter(department__code=department)
        
        # Filter by designation if specified
        designation = self.request.GET.get('designation')
        if designation:
            queryset = queryset.filter(designation=designation)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['designations'] = Faculty.DESIGNATION_CHOICES
        context['selected_department'] = self.request.GET.get('department', '')
        context['selected_designation'] = self.request.GET.get('designation', '')
        return context

class FacultyDetailView(DetailView):
    """Detail view for individual faculty member"""
    model = Faculty
    template_name = 'accounts/faculty_detail.html'
    context_object_name = 'faculty'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get courses taught by this faculty member
        from courses.models import Course
        context['courses'] = Course.objects.filter(instructor=self.object)
        return context