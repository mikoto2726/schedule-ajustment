from django.shortcuts import render, redirect
from .forms import ScheduleForm, CreateDateOptionForm, DateOptionFormSet
from .models import Member, DateOption

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
        formset = DateOptionFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('schedule') 
    else:
        formset = DateOptionFormSet(queryset=DateOption.objects.none())
    return render(request, 'schedule/create_date.html', {'formset': formset})