from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class Event(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    max_attendees = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def save(self, *args, **kwargs):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")
        super().save(*args, **kwargs)


class Attendee(models.Model):
    attendee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    check_in_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
