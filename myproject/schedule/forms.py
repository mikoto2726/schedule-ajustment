from django import forms
from .models import Event, Participant
from datetime import datetime
from django.core.exceptions import ValidationError

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']

class MultipleDatesForm(forms.Form):
    title = forms.CharField(max_length=200, label="タイトル", widget=forms.TextInput(attrs={'placeholder': 'イベントのタイトル'}))
    description = forms.CharField(label="説明", widget=forms.Textarea(attrs={'placeholder': 'イベントの説明'}))
    dates = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '日付を選択'}))
    
    def clean_dates(self):
        data = self.cleaned_data['dates']
        date_list = [date.strip() for date in data.split(',')]
        
        # 日付の形式を検証
        for date_str in date_list:
            try:
                datetime.strptime(date_str, '%m-%d')
            except ValueError:
                raise ValidationError(f'{date_str} は有効な日付形式ではありません。YYYY-MM-DD形式で入力してください。')

        return date_list

