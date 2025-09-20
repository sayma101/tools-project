"""
Courses app URLs
"""
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/enroll/', views.EnrollView.as_view(), name='enroll'),
    path('<int:pk>/unenroll/', views.UnenrollView.as_view(), name='unenroll'),
    path('my-courses/', views.MyCoursesView.as_view(), name='my_courses'),
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
]