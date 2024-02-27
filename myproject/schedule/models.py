from django.db import models
from django.utils.formats import date_format
# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slack_id = models.CharField(max_length=20, primary_key=True)
    date_options = models.ManyToManyField('DateOption', related_name='members')
    def __str__(self):
        return self.name
    
class DateOption(models.Model):
    date = models.DateField(unique=True)
    participants = models.ManyToManyField('Member', related_name='available_dates')

    def __str__(self):
        weekdays = ['月', '火', '水', '木', '金', '土', '日']
        weekday_str = weekdays[self.date.weekday()]
        return f"{self.date} ({weekday_str})"