from django import forms
from .models import Member, EventDate, Event, Participant, DateOption
from datetime import datetime
from django.core.exceptions import ValidationError

class MultipleDatesForm(forms.Form):
    title = forms.CharField(max_length=200, label="タイトル", widget=forms.TextInput(attrs={'placeholder': 'イベントのタイトル'}))
    description = forms.CharField(max_length=200, label="説明", widget=forms.TextInput(attrs={'placeholder': 'イベントの説明'}))
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

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description']

class EventDateForm(forms.ModelForm):
    class Meta:
        model = EventDate
        fields = ['date']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']


class AnswerForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Member.objects.all(), empty_label="名前を選択")
    dates = forms.ModelMultipleChoiceField(queryset=EventDate.objects.none(), widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, event=None, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        if event is not None:
            self.fields['dates'].queryset = EventDate.objects.filter(event=event)