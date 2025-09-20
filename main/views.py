"""
Main app views for university website
"""
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import ContactMessage, GalleryImage, GalleryVideo, UniversityInfo
from .forms import ContactForm
from accounts.models import Faculty
from courses.models import Course
from events.models import Event

class HomeView(TemplateView):
    """Home page view with university overview"""
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get university info
        try:
            context['university_info'] = UniversityInfo.objects.first()
        except UniversityInfo.DoesNotExist:
            context['university_info'] = None
        
        # Get featured content
        context['featured_faculty'] = Faculty.objects.filter(is_featured=True)[:3]
        context['recent_events'] = Event.objects.filter(is_published=True)[:3]
        context['featured_courses'] = Course.objects.filter(is_featured=True)[:6]
        context['featured_images'] = GalleryImage.objects.filter(is_featured=True)[:6]
        
        return context

class AboutView(TemplateView):
    """About page view"""
    template_name = 'main/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            context['university_info'] = UniversityInfo.objects.first()
        except UniversityInfo.DoesNotExist:
            context['university_info'] = None
            
        context['faculty_members'] = Faculty.objects.all()[:8]
        
        return context

class ContactView(TemplateView):
    """Contact page view with form handling"""
    template_name = 'main/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        
        try:
            context['university_info'] = UniversityInfo.objects.first()
        except UniversityInfo.DoesNotExist:
            context['university_info'] = None
            
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('main:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})

class GalleryView(TemplateView):
    """Gallery page view with images and videos"""
    template_name = 'main/gallery.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all gallery items with pagination
        images = GalleryImage.objects.all()
        videos = GalleryVideo.objects.all()
        
        # Paginate images
        image_paginator = Paginator(images, 12)
        image_page = self.request.GET.get('image_page', 1)
        context['images'] = image_paginator.get_page(image_page)
        
        # Paginate videos
        video_paginator = Paginator(videos, 8)
        video_page = self.request.GET.get('video_page', 1)
        context['videos'] = video_paginator.get_page(video_page)
        
        return context

class SearchView(TemplateView):
    """Search functionality across the website"""
    template_name = 'main/search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        
        if query:
            # Search in courses
            courses = Course.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(department__name__icontains=query)
            )
            
            # Search in faculty
            faculty = Faculty.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(department__name__icontains=query) |
                Q(specialization__icontains=query)
            )
            
            # Search in events
            events = Event.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query),
                is_published=True
            )
            
            context.update({
                'query': query,
                'courses': courses,
                'faculty': faculty,
                'events': events,
                'total_results': courses.count() + faculty.count() + events.count()
            })
        
        return context