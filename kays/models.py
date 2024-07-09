from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone


class team(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()

class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.subject
    
class Testimony(models.Model):
    content = models.TextField()
    client_name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimony_images/', blank=True, null=True)

    def __str__(self):
        return self.client_name
    

    
class Room(models.Model):
    room_name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return self.room_name

class Booking(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    email = models.EmailField()
    num_guests = models.IntegerField(default=1)
    special_request = models.TextField(max_length=200, default="")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Booking)
def check_room_availability(sender, instance, **kwargs):
   
    overlapping_bookings = Booking.objects.filter(room=instance.room).filter(
        check_in__lt=instance.check_out,
        check_out__gt=instance.check_in 
    ).exclude(pk=instance.pk)  
    if overlapping_bookings.exists():
        raise ValidationError('This room is already booked for the selected dates.')

    if instance.check_in >= instance.check_out:
        raise ValidationError('Check-in date must be before check-out date.')
    
