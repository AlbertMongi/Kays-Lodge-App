# views.py
from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse
import json
from .models import team
from .models import Room
from .forms import SubscriberForm
from .forms import ContactForm
from django.contrib import messages
from django.http import JsonResponse
from .forms import BookingForm  # Assuming you have created a form for the Booking model
from .models import Booking
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, HttpResponse
from .forms import SubscriberForm, ContactForm
from .models import ContactMessage
from .models import Testimony
from django.db.models import Q


from django.utils.html import strip_tags


# def index(request):
#     # Retrieve all teams
#     teams = team.objects.all()
    
#     # Retrieve all testimonies
#     testimonies = Testimony.objects.all()
    
#     # Handling form submission for newsletter subscription
#     success_message = None
#     if request.method == 'POST':
#         form = SubscriberForm(request.POST)
#         if form.is_valid():
#             form.save()
#             success_message = 'You have successfully subscribed to our newsletter'
#     else:
#         form = SubscriberForm()
    
#     # Render the index.html template with necessary context data
#     return render(request, "index.html", {'teams': teams, 'form': form, 'success_message': success_message, 'testimonies': testimonies})
def index(request):
    # Retrieve all teams
    teams = team.objects.all()  # Corrected model name to Team
    
    # Retrieve all testimonies
    testimonies = Testimony.objects.all()
    
    # Handling form submission for newsletter subscription
    success_message = None
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'You have successfully subscribed to our newsletter'
            form = SubscriberForm()  # Reset form after successful submission
    else:
        form = SubscriberForm()
    
    # Render the index.html template with necessary context data
    return render(request, "index.html", {'teams': teams, 'form': form, 'success_message': success_message, 'testimonies': testimonies})

def about(request):
    teams = team.objects.all()  # Retrieve all teams
    success_message = None
    
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'You have successfully subsribed our newsletter'
    else:
        form = SubscriberForm()
    
    return render(request, "about.html", {'teams': teams, 'form': form, 'success_message': success_message})

def rooms(request):
    teams = team.objects.all()  # Retrieve all teams
    success_message = None
    
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'You have successfully subsribed our newsletter'
    else:
        form = SubscriberForm()
    
    return render(request, "rooms.html", {'form': form, 'success_message': success_message})


def services(request):
    teams = team.objects.all()  # Retrieve all teams
    success_message = None
    testimonies = Testimony.objects.all()
    
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'You have successfully subscribed to our newsletter'
    else:
        form = SubscriberForm()
    
    return render(request, "services.html", {'form': form, 'success_message': success_message, 'testimonies': testimonies})

  
def gallery(request):
    teams = team.objects.all()  # Retrieve all teams
    success_message = None
    
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'You have successfully subsribed our newsletter'
    else:
        form = SubscriberForm()
    
    return render(request, "gallery.html", {'form': form, 'success_message': success_message})


def testimonials(request):
    Testimonies = Testimony.objects.all()
    return render(request, 'services.html', {'testimonies': Testimonies})

def booking(request):
    

    message = "Your Booking has been received, Thanks"
    data = {
            'subject': "Booking Confirmation",
            'message': message
    }
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
           
            send_mail(data['subject'], message,'' ,[form.cleaned_data['email']], fail_silently=False,)


            # Redirect to a confirmation page
            return redirect(booking_confirmation_view)
    else:
        form = BookingForm()
    return render(request, 'booking.html', {'form': form})

def booking_confirmation_view(request):
    # Render a confirmation page
    return render(request, 'booking_confirmation.html')

def contact(request):
    success_message_contact = None
    success_message_services = None
    contact_form = ContactForm()
    subscriber_form = SubscriberForm()

    if request.method == 'POST':
        if 'name' in request.POST and 'email' in request.POST and 'message' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                success_message_contact = 'Thank you for your message!'
                return JsonResponse({'success_message_contact': success_message_contact})
            else:
                errors = {field: errors[0] for field, errors in contact_form.errors.items()}
                return JsonResponse({'errors': errors}, status=400)
        elif 'email' in request.POST:
            subscriber_form = SubscriberForm(request.POST)
            if subscriber_form.is_valid():
                subscriber_form.save()
                success_message_services = 'You have successfully subscribed to our newsletter'
                return JsonResponse({'success_message_services': success_message_services})
            else:
                errors = {field: errors[0] for field, errors in subscriber_form.errors.items()}
                return JsonResponse({'errors': errors}, status=400)

    teams = team.objects.all()

    return render(request, "contact.html", {
        'contact_form': contact_form,
        'subscriber_form': subscriber_form,
        'teams': teams
    })

# def check_available_rooms(request):
#     if request.method == 'POST':
#         data = json.loads(list(request.POST.keys())[0])
#         check_in_date = datetime.strptime(data['check_in'], '%d-%m-%Y').date()

#         all_rooms = Room.objects.all()

#         booked2 = Booking.objects.all()

#         print('Booking', booking)

#         booked_rooms = Booking.objects.filter(
#             Q(check_in__lte=check_in_date, check_out__gt=check_in_date)
#         ).values_list('room_id', flat=True)

#         print('Booked', booked_rooms)

#         unbooked_rooms = all_rooms.exclude(id__in=booked_rooms)

#         room_data = list(unbooked_rooms.values('id', 'room_name', 'price'))  # Serialize queryset to list

#         return JsonResponse({'unbooked_rooms': room_data})

#     return JsonResponse({'error': 'Invalid request'}, status=400)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import Room, Booking

@csrf_exempt
def check_available_rooms(request):
    if request.method == "POST":
        data = json.loads(request.body)
        check_in = parse_datetime(data.get('check_in'))
        check_out = parse_datetime(data.get('check_out'))
        
        
        booked_rooms = Booking.objects.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).values_list('room_id', flat=True)
        
        available_rooms = Room.objects.exclude(id__in=booked_rooms)
        
        room_list = [{'id': room.id, 'name': room.room_name} for room in available_rooms]
        
        return JsonResponse({'rooms': room_list})
    return JsonResponse({'error': 'Invalid request'}, status=400)
