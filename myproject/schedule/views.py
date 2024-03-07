from django.shortcuts import redirect, render, get_object_or_404
from .forms import EventForm, ParticipantForm, MultipleDatesForm
from .models import Event, EventDate
from datetime import datetime
from django.views.decorators.http import require_http_methods

def event_list(request):
    events = Event.objects.prefetch_related('dates').all()
    return render(request, 'schedule/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'schedule/event_detail.html', {'event': event})


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
    return render(request, 'schedule/event_edit.html', {'form': form})

def success(request):
    return render(request, 'schedule/success.html')

@require_http_methods(["POST"])  # POSTリクエストのみを許可
def delete_all_dates(request):
    # DateOptionモデルの全インスタンスを削除
    Event.objects.all().delete()
    return redirect('event_list')