from django.shortcuts import render, redirect, get_object_or_404
from .forms import AnswerForm, MultipleDatesForm, EventForm, ParticipantForm
from .models import Member, DateOption, Event, EventDate, Participant
from datetime import datetime
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import IntegrityError

def index(request):
    return render(request, 'schedule/index.html')

def answer(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST, event=event)
        if form.is_valid():
            # Formから選択されたMemberのインスタンスを取得
            selected_member = form.cleaned_data['name']
            selected_dates = form.cleaned_data['dates']

        
            # 選択された日付に対して参加者を関連付ける
            for date in selected_dates:
                date.participants.add(selected_member)  # EventDateにparticipantsフィールドが存在すると仮定
                date.save()

            return redirect('success')  # 成功時のリダイレクト先
    else:
        form = AnswerForm(event=event)
    return render(request, 'schedule/answer.html', {'form': form, 'event': event})

def success(request):
    return render(request, 'schedule/success.html')

def results(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event_dates_with_participants = EventDate.objects.filter(event=event).prefetch_related('participants')
    most_participants = max(event_dates_with_participants, key=lambda d: d.participants.count(), default=None)
    context = {
        'event': event,
        'event_dates_with_participants': event_dates_with_participants,
        'most_participants': most_participants,
    }
    return render(request, 'schedule/results.html', context)


def delete_date(request, date_str):
    if request.method == "POST":
        # 文字列から日付オブジェクトを作成
        date_obj = datetime.strptime(date_str, '%m-%d').date()
        # 日付に一致するDateOptionインスタンスを検索
        date_option = get_object_or_404(DateOption, date=date_obj)
        date_option.delete()  # インスタンスを削除
        return redirect('results')
    else:
        return HttpResponseForbidden()

def list(request):
    events = Event.objects.prefetch_related('dates').all()
    return render(request, 'schedule/list.html', {'events': events})

def detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'schedule/detail.html', {'event': event})


def create(request):
    if request.method == 'POST':
        form = MultipleDatesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            dates = form.cleaned_data['dates']
            event = Event.objects.create(title=title, description=description)
            for date_str in dates:
                date = datetime.strptime(date_str, '%m-%d').date()
                EventDate.objects.create(event=event, date=date)
            return redirect('list')  # 'your_success_url'は成功時にリダイレクトするURLの名前です。
    else:
        form = MultipleDatesForm()
    return render(request, 'schedule/create.html', {'form': form})

@require_http_methods(["POST"])  # POSTリクエストのみを許可
def delete_all_event(request):
    Event.objects.all().delete()
    return redirect('list')

@require_http_methods(["POST"])  # POSTリクエストのみを許可
def delete_all_dates(request):
    DateOption.objects.all().delete()
    return redirect('results')