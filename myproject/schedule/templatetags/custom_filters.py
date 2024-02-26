from django import template
import datetime

register = template.Library()

@register.filter(name='weekday')
def weekday(value):
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    return weekdays[value.weekday()]
