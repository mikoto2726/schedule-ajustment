from django import forms
from .models import Member, DateOption
from django.forms import modelformset_factory


DateOptionFormSet = modelformset_factory(
    DateOption,
    fields=('date',),
    extra=3,
    widgets={'date': forms.DateInput(attrs={'type': 'date'})}
)

class ScheduleForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Member.objects.all(), empty_label="名前を選択")
    dates = forms.ModelMultipleChoiceField(queryset=DateOption.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dates'].queryset = DateOption.objects.all()

class CreateDateOptionForm(forms.ModelForm):
    class Meta:
        model = DateOption
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }