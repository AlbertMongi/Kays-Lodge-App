# views.py
from datetime import datetime
from django.conf import settings
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


def booking_confirmation_view(request):
    # Render a confirmation page
    # return render(request, 'booking_confirmation.html')
     return render(request, 'Bookingconf.html')

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


import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_POST
from .models import Booking, Room
from .forms import BookingForm

@require_POST
def check_available_rooms(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        check_in = parse_datetime(data.get('check_in'))
        check_out = parse_datetime(data.get('check_out'))
        
        if not check_in or not check_out:
            return JsonResponse({'error': 'Invalid date format for check_in or check_out'}, status=400)
        
        # Filter bookings overlapping with the requested period
        booked_rooms = Booking.objects.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).values_list('room_id', flat=True)
        
        # Exclude booked rooms from available rooms
        available_rooms = Room.objects.exclude(id__in=booked_rooms)
        
        # Construct JSON response with room information
        room_list = [{'id': room.id, 'name': room.room_name, 'price': room.price} for room in available_rooms]
        
        return JsonResponse({'rooms': room_list})
    
    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'Invalid JSON format: {str(e)}'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save form data to the database
            booking_instance = form.save(commit=False)  # Don't save yet, we'll customize the email message first
            booking_instance.status = 'Not Paid'  # Set status as 'Not Paid' by default 

            # Retrieve room_id and calculate room_price from the database
            room_id = form.cleaned_data['room'].id
            room = Room.objects.get(id=room_id)
            room_price = room.price

            # Calculate total amount of days
            check_in_date = form.cleaned_data['check_in']
            check_out_date = form.cleaned_data['check_out']
            total_days = (check_out_date - check_in_date).days

            # Calculate additional amount based on conditions
            additional_amount = calculate_additional_amount(room, room_price, form.cleaned_data['num_guests'])

            # Calculate total price including additional amount
            total_price = (room_price + additional_amount) * total_days

            # Customize email message with booking details
            subject = "Reservation Confirmation"
            message = f"""Dear Guest(s),

Thank you for reserving your room(s) with Kays Lodge, Msasani Village. We are excited to welcome you and ensure your comfort and relaxation at our family-run lodge.

Here are your Reservation Details:
----------------------------------
Name: {form.cleaned_data['name']}
Surname: {form.cleaned_data['surname']}
Room: {form.cleaned_data['room']} 
Check-in Date: {check_in_date}
Check-out Date: {check_out_date}
Number of Guests: {form.cleaned_data['num_guests']}
Total Amount: ${total_price} 
Status: Not Paid
Special Request: {form.cleaned_data['special_request']}

Please read our terms and conditions below:
Terms and Conditions:
--------------------
Guest stay conditions:
- All room bookings are subject to Government of Tanzanian laws which stipulates that same sex guests may not stay in Double rooms. However, same sex guests may stay in our Twin Double room.
- All children under the age of 10 years old may sleep with their parents. All above this age are expected to have independent bedrooms during their stay. Same conditions would apply for same sex restrictions where a child is 10 years old or above sleeping with an adult. I.e., Twin bedroom would be required. 
- We do not permit smoking in the bedrooms or bathrooms.
- We do not permit pets in the compound unless they are caged pets which will not make any noise and are placed in our designated area outside in open air.  

Liability:
- Please note guests will be liable for paying for the remainder of their stay if they break rules, do not fulfil conditions of Guest stay or bring pets which later are found to make noise for other guests.   

Booking and Reservations:
- Booking refers to paid room stay which is made through our sister partner booking.com or through international money transfer to our account with CRDB Bank Tanzania (email to info@kayslodge.co.tz for bank details. Always include Name and arrival date in your payment reference). 
- Reservations refers to unpaid room stay.

Cancellation Policy:
- All reservations may be subject to cancellations by Kays lodge in case of increased room demands. Please book your room through Booking.com to avoid disappointment.
- In case of booked rooms, cancellations made by guests 48 hours before date of arrival by email to info@kayslodge.co.tz will not be charged for their stay.
- Payment will be taken for cancellations made less than 48 hours before the date of arrival. A fee applied will be 50% of the total period of guest's nights' stay up to 7 nights of their initial stay. Any stay beyond 7 nights after date of arrival will receive full 100% refund.

We look forward to hosting you!

Sincerely,
Kays Lodge Team.
            """

            # Send the email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [form.cleaned_data['email']], fail_silently=False)

            # Save the booking instance to database after customizing the email message
            booking_instance.save()

            # Redirect to a confirmation page after successful submission
            return redirect('booking_confirmation_view')  # Replace 'booking_confirmation_view' with your actual URL name or path
    else:
        form = BookingForm()

    return render(request, 'booking.html', {'form': form})

def calculate_additional_amount(room_name, room_price, num_guests):
    additional_amount = 0
    # Add logic for additional amount based on room or guest conditions if needed
    if (room_name != 'Room no.1 - Standard Single Room' 
        and room_name != 'Room no.5 - Standard Single Room' 
        and room_name != 'Room no.6 - Standard Single Room' 
        and room_name != 'Room no.15 - Deluxe Single Room'):

        if room_name == 'Room no.7 - Standard Twin Room' and num_guests == 2:
            additional_amount = 11
        elif room_price == 40 and num_guests == 2:
            additional_amount = 6
        elif room_price == 35 and num_guests == 2:
            additional_amount = 5

    return additional_amount
