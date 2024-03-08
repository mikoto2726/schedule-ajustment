from django.db import models
from django.utils.dateformat import DateFormat

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
class EventDate(models.Model):
    event = models.ForeignKey(Event, related_name='dates', on_delete=models.CASCADE)
    date = models.DateField()
    def __str__(self):
        df = DateFormat(self.date)
        return df.format('m月d日')  # or your preferred format
    
class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Response(models.Model):
    participant = models.ForeignKey(Participant, related_name='responses', on_delete=models.CASCADE)
    event_date = models.ForeignKey(EventDate, on_delete=models.CASCADE)
    availability = models.BooleanField()  # True for available, False for not available