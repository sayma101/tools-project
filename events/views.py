"""
Events app views for events and announcements
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Event, Announcement, EventRegistration
from accounts.models import Department

class EventListView(ListView):
    """List view for all events"""
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Event.objects.filter(is_published=True).select_related(
            'organizer', 'department'
        )
        
        # Filter by event type
        event_type = self.request.GET.get('type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        # Filter by department
        department = self.request.GET.get('department')
        if department:
            queryset = queryset.filter(department__code=department)
        
        # Filter by time period
        time_filter = self.request.GET.get('time', 'all')
        now = timezone.now()
        
        if time_filter == 'upcoming':
            queryset = queryset.filter(start_date__gt=now)
        elif time_filter == 'ongoing':
            queryset = queryset.filter(start_date__lte=now, end_date__gte=now)
        elif time_filter == 'past':
            queryset = queryset.filter(end_date__lt=now)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = Event.EVENT_TYPES
        context['departments'] = Department.objects.all()
        context['filters'] = {
            'type': self.request.GET.get('type', ''),
            'department': self.request.GET.get('department', ''),
            'time': self.request.GET.get('time', 'all'),
            'search': self.request.GET.get('search', ''),
        }
        context['featured_events'] = Event.objects.filter(
            is_featured=True,
            is_published=True,
            start_date__gt=timezone.now()
        )[:3]
        return context

class EventDetailView(DetailView):
    """Detail view for individual event"""
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        return Event.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        # Check if user is registered
        if self.request.user.is_authenticated:
            context['is_registered'] = EventRegistration.objects.filter(
                event=event,
                user=self.request.user
            ).exists()
        else:
            context['is_registered'] = False
        
        # Get related events
        context['related_events'] = Event.objects.filter(
            event_type=event.event_type,
            is_published=True
        ).exclude(pk=event.pk)[:3]
        
        return context

class EventCalendarView(TemplateView):
    """Calendar view for events"""
    template_name = 'events/event_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get events for the current month
        now = timezone.now()
        events = Event.objects.filter(
            is_published=True,
            start_date__year=now.year,
            start_date__month=now.month
        ).select_related('organizer', 'department')
        
        context['events'] = events
        context['current_month'] = now.strftime('%B %Y')
        
        return context

class AnnouncementListView(ListView):
    """List view for all announcements"""
    model = Announcement
    template_name = 'events/announcement_list.html'
    context_object_name = 'announcements'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Announcement.objects.filter(is_published=True).select_related(
            'author', 'department'
        )
        
        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by department
        department = self.request.GET.get('department')
        if department:
            queryset = queryset.filter(department__code=department)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(target_audience__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['priorities'] = Announcement.PRIORITY_CHOICES
        context['departments'] = Department.objects.all()
        context['filters'] = {
            'priority': self.request.GET.get('priority', ''),
            'department': self.request.GET.get('department', ''),
            'search': self.request.GET.get('search', ''),
        }
        context['pinned_announcements'] = Announcement.objects.filter(
            is_pinned=True,
            is_published=True
        )[:3]
        return context

class AnnouncementDetailView(DetailView):
    """Detail view for individual announcement"""
    model = Announcement
    template_name = 'events/announcement_detail.html'
    context_object_name = 'announcement'
    
    def get_queryset(self):
        return Announcement.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        announcement = self.get_object()
        
        # Get related announcements
        context['related_announcements'] = Announcement.objects.filter(
            department=announcement.department,
            is_published=True
        ).exclude(pk=announcement.pk)[:3]
        
        return context