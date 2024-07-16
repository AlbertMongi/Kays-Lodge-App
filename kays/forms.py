# forms.py

from django import forms
from .models import Subscriber
from .models import ContactMessage
from .models import Booking
from .models import Testimony

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimony
        fields = ['content', 'client_name', 'profession', 'image']

# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['name', 'surname', 'check_in', 'check_out', 'email', 'num_guests', 'special_request']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'surname', 'check_in', 'check_out', 'email', 'num_guests', 'room', 'special_request']
        widgets = {
            'check_in': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#checkin'}),
            'check_out': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#checkout'}),
            
        } 