from django.urls import path
from . import views 
from django.contrib.sitemaps.views import sitemap
from kays_lodge.sitemaps import StaticSitemap, PostViewSitemap  # Make sure you have this import
from django.views.generic.base import TemplateView
sitemaps = {
    'static': StaticSitemap,
    'posts': PostViewSitemap,
}

urlpatterns = [
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
     path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path("", views.index, name='index'),
    path('about/', views.about, name="about"),  # Added trailing slash
    path('services/', views.services, name="services"),  # Added trailing slash
    path('booking/', views.booking, name="booking"),  # Added trailing slash
    path('booking/available-rooms/', views.check_available_rooms, name="check_available_rooms"),  # Added trailing slash
    path('contact/', views.contact, name="contact"),  # Added trailing slash
    path('rooms/', views.rooms, name="rooms"),  # Added trailing slash
    path('gallery/', views.gallery, name="gallery"),  # Added trailing slash
    path('booking_confirmation_view/', views.booking_confirmation_view, name="booking_confirmation_view")  # Corrected any potential trailing slash issue
]
