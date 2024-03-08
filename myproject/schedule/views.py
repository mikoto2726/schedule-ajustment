from django.shortcuts import render, redirect, get_object_or_404
from .forms import AnswerForm, MultipleDatesForm, EventForm, ParticipantForm
from .models import Member, DateOption, Event, EventDate
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
            selected_name = form.cleaned_data['name']
            selected_dates = form.cleaned_data['dates']
            member = Member.objects.get(name=selected_name)
            valid_dates = EventDate.objects.filter(id__in=[date.id for date in selected_dates])
            date_ids = [date.id for date in valid_dates]
            try:
                member.available_dates.clear()
                member.available_dates.set(date_ids)
            except IntegrityError:
                pass
            member.save()
            return redirect('success')  # 成功時のリダイレクト先
    else:
        form = AnswerForm(event=event)
    return render(request, 'schedule/answer.html', {'form': form, 'event': event})

def success(request):
    return render(request, 'schedule/success.html')

def results(request):
    dates_with_participants = DateOption.objects.prefetch_related('participants').order_by('date').all()
    most_participants = max(dates_with_participants, key=lambda d: d.participants.count(), default=None)
    context = {
        'dates_with_participants': dates_with_participants,
        'most_participants': most_participants
    }
    return render(request, 'schedule/results.html', context)

def delete_date(request, date_str):
    if request.method == "POST":
        # 文字列から日付オブジェクトを作成
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
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