from django.db import models
from django.utils.formats import date_format
from django.db.models import Max
from django.db import transaction
# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slack_id = models.CharField(max_length=20, primary_key=True)
    def __str__(self):
        return self.name
    
def get_default_session():
    # ScheduleSessionの最後のインスタンスのIDを取得
    max_id = ScheduleSession.objects.aggregate(max_id=Max('id'))['max_id']
    if max_id is not None:
        return max_id
    else:
        with transaction.atomic():
            # デフォルトのScheduleSessionインスタンスを作成
            default_session = ScheduleSession.objects.create(title="デフォルトセッション", description="自動生成されたデフォルトセッション")
            return default_session.id
    
class ScheduleSession(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    dates = models.ManyToManyField('DateOption', related_name='sessions')

    def __str__(self):
        return self.title

class DateOption(models.Model):
    date = models.DateField(unique=True)
    participants = models.ManyToManyField('Member', related_name='available_dates')
    
    def __str__(self):
        weekdays = ['月', '火', '水', '木', '金', '土', '日']
        weekday_str = weekdays[self.date.weekday()]
        return f"{self.date} ({weekday_str})"
    
