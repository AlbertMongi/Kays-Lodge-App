from django.urls import path
from . import views 

urlpatterns = [
    path("", views.index, name='index'),
    path('about', views.about, name="about"),
    path('services', views.services, name="services"),
    path('booking', views.booking, name="booking"),
    path('booking/available-rooms', views.check_available_rooms, name="check_available_rooms"),
    path('contact', views.contact, name="contact"),
    path('rooms', views.rooms, name="rooms"),
    path('gallery', views.gallery, name="gallery"),
    path('booking_confirmation_view/', views.booking_confirmation_view, name="booking_confirmation_view")

]
