from django.contrib import admin
from Event.models import Event, Attendee
# Register your models here.

admin.site.register(Event)
admin.site.register(Attendee)