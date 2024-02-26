from django import forms
from .models import Member, DateOption, ScheduleSession
from datetime import datetime

class ScheduleForm(forms.Form):#日程調整に回答する時用
    session = forms.ModelChoiceField(queryset=ScheduleSession.objects.all(), empty_label="日程調整を選択", label="日程調整")
    name = forms.ModelChoiceField(queryset=Member.objects.all(), empty_label="名前を選択", label="名前")
    dates = forms.ModelMultipleChoiceField(queryset=DateOption.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label="日程")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dates'].queryset = DateOption.objects.all()

class CreateDateOptionForm(forms.ModelForm):
    title = forms.CharField(max_length=100, label="日程調整のタイトル")
    description = forms.CharField(max_length=100, label="日程調整の説明", required=False)
    dates = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ScheduleSession
        fields = ['title', 'description', 'dates'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # 'dates' フィールドのデータを解析して関連付ける
            date_strings = self.cleaned_data.get('dates', [])
            for date_string in date_strings:
                date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()
                date_option, created = DateOption.objects.get_or_create(date=date_obj)
                instance.dates.add(date_option)
        return instance

    
class ScheduleSessionForm(forms.ModelForm):
    class Meta:
        model = ScheduleSession
        fields = ['title', 'description', 'dates']
        widgets = {
            'dates': forms.CheckboxSelectMultiple,
        }