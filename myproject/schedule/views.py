from django.shortcuts import redirect, render, get_object_or_404
from .forms import EventForm, ParticipantForm, MultipleDatesForm, ResponseForm
from .models import Event, EventDate, Participant, Response
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Q

def event_list(request):
    events = Event.objects.prefetch_related('dates').all()
    return render(request, 'schedule/list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'schedule/detail.html', {'event': event})


def your_view(request):
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
            return redirect('event_list')  # 'your_success_url'は成功時にリダイレクトするURLの名前です。
    else:
        form = MultipleDatesForm()
    return render(request, 'schedule/create.html', {'form': form})

@require_http_methods(["POST"])  # POSTリクエストのみを許可
def delete_all_dates(request):
    # DateOptionモデルの全インスタンスを削除
    Event.objects.all().delete()
    return redirect('event_list')

def respond_to_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            participant_name = request.POST.get('participant_name')  # または適切な方法で参加者の名前を取得
            if participant_name:  # participant_name が空でないことを確認
                participant, created = Participant.objects.get_or_create(name=participant_name, event=event)
                response.participant = participant
                response.save()
                return redirect('schedule/view_event_results', event_id=event_id)
    else:
        form = ResponseForm()
    return render(request, 'schedule/respond_to_event.html', {'form': form, 'event': event})

def view_event_results(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event_dates = EventDate.objects.filter(event__id=event_id).annotate(
        available_count=Count('response', filter=Q(response__availability=True)),
        unavailable_count=Count('response', filter=Q(response__availability=False))
    )
    return render(request, 'schedule/event_results.html', {'event': event, 'event_dates': event_dates})