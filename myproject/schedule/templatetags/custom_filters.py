from django import template
import datetime

register = template.Library()

@register.filter(name='weekday')
def weekday(value):
    if isinstance(value, str):
        try:
            value = datetime.datetime.strptime(value, '%y-%m-%d').date()  # '%y-%m-%d' 形式に修正
        except ValueError:
            return '日付形式が正しくありません'  # 日付形式が正しくない場合は空文字を返す
    weekdays = ['火', '水', '木', '金', '土', '日', '月']
    if isinstance(value, datetime.date):
        return weekdays[value.weekday()]
    return ''