from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),                  # Main landing profile overview
    path('history/', views.experience_view, name='history'), # Explicit Career Timeline
    path('projects/', views.projects_view, name='projects'), # Data Engineering Pipelines
    path('services/', views.services_view, name='services'), # Newcomer & Student Services Hub
    path('contact/', views.contact_view, name='contact'),    # Booking interface
]