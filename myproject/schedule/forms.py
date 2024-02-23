from django import forms
from .models import Member, DateOption

class ScheduleForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Member.objects.all(), empty_label="名前を選択")
    dates = forms.ModelMultipleChoiceField(queryset=DateOption.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dates'].queryset = DateOption.objects.all()

class CreateDateOptionForm(forms.Form):
    dates = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'multiple': True}))

    def clean_dates(self):
        dates_str = self.cleaned_data['dates']
        date_list = [date_str.strip() for date_str in dates_str.split(',')]
        return date_list