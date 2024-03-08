from django.db import models
from django.utils.formats import date_format


class Member(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slack_id = models.CharField(max_length=20, primary_key=True)
    def __str__(self):
        return self.name
    
class DateOption(models.Model):
    date = models.DateField(unique=True)
    participants = models.ManyToManyField('Member', related_name='available_dates')

    def __str__(self):
        weekdays = ['月', '火', '水', '木', '金', '土', '日']
        weekday_str = weekdays[self.date.weekday()]
        return f"{self.date} ({weekday_str})"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

class EventDate(models.Model):
    event = models.ForeignKey(Event, related_name='dates', on_delete=models.CASCADE)
    date = models.DateField()
    participants = models.ManyToManyField('Member', related_name='participating_dates')
    def __repr__(self):
        return f"EventDate({self.date.month}, {self.date.day})"

    def __str__(self):
        return f"{self.date.month}-{self.date.day}"
    
class EventParticipant(models.Model):
    event_date = models.ForeignKey(EventDate, on_delete=models.CASCADE, related_name='event_participants')
    participant = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='event_dates')

    def __str__(self):
        return f"{self.event_date} - {self.participant}"
