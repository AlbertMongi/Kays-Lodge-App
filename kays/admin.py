from django.contrib import admin
from .models import team
from .models import Subscriber
from .models import ContactMessage
from .models import Booking
from .models import Room
from .models import Testimony
# Register your models here.


admin.site.register(team)

admin.site.register(Subscriber)


admin.site.register(ContactMessage)

admin.site.register(Booking)

admin.site.register(Room)


admin.site.register(Testimony)

