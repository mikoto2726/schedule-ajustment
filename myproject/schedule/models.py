from django.db import models

# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slack_id = models.CharField(max_length=20, primary_key=True)
    def __str__(self):
        return self.name
    
class DateOption(models.Model):
    date = models.DateField()
    participants = models.ManyToManyField('Member', related_name='available_dates')

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')