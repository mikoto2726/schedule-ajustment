from django import forms
from .models import Member, DateOption
from datetime import datetime

class ScheduleForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Member.objects.all(), empty_label="名前を選択")
    dates = forms.ModelMultipleChoiceField(queryset=DateOption.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dates'].queryset = DateOption.objects.all()

class CreateDateOptionForm(forms.Form):
    dates = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'multiple': True}))

    def clean_dates(self):
        # 入力された日付の文字列をリストに変換
        dates_str = self.cleaned_data['dates']
        date_list_str = [date_str.strip() for date_str in dates_str.split(',')]

        # 文字列を日付型に変換し、日付順にソート
        date_list = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in date_list_str]
        date_list.sort()

        # ソートされた日付リストを、再び文字列のリストに変換して返す（必要に応じて）
        sorted_date_list_str = [date.strftime('%Y-%m-%d') for date in date_list]
        return sorted_date_list_str