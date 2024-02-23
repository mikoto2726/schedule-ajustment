from django.shortcuts import render, redirect, get_object_or_404
from .forms import ScheduleForm, CreateDateOptionForm
from .models import Member, DateOption
from datetime import datetime
from django.http import HttpResponseForbidden
from django.db.models import Q

def index(request):
    return render(request, 'schedule/index.html')

def schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            selected_name = form.cleaned_data['name']
            selected_dates = form.cleaned_data['dates']
            member = Member.objects.get(name=selected_name)
            member.available_dates.set(selected_dates)
            member.save()
            return redirect('success')  # 成功時のリダイレクト先
    else:
        form = ScheduleForm()
    return render(request, 'schedule/schedule_form.html', {'form': form})

def success(request):
    return render(request, 'schedule/success.html')

def create_date(request):
    if request.method == 'POST':
        form = CreateDateOptionForm(request.POST)
        if form.is_valid():
            date_list = form.cleaned_data['dates']
            for date_str in date_list:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                DateOption.objects.create(date=date_obj)
    else:
        form = CreateDateOptionForm()

    return render(request, 'schedule/create_date.html', {'form': form})

def view_results(request):
    # 各日付とその日付に参加するメンバーのリストを取得
    dates_with_participants = DateOption.objects.prefetch_related('participants').all()

    # 最も参加者の多い日付を見つける
    most_participants = max(dates_with_participants, key=lambda d: d.participants.count(), default=None)

    context = {
        'dates_with_participants': dates_with_participants,
        'most_participants': most_participants
    }
    return render(request, 'schedule/view_results.html', context)

def delete_date(request, date_str):
    if request.method == "POST":
        # 文字列から日付オブジェクトを作成
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        # 日付に一致するDateOptionインスタンスを検索
        date_option = get_object_or_404(DateOption, date=date_obj)
        date_option.delete()  # インスタンスを削除
        return redirect('view_results')
    else:
        return HttpResponseForbidden()