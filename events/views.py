from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from events.forms import UserRegistrationForm, EventForm
from django.utils import timezone
from .models import Event
from datetime import date

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index2')
    return render(request, 'login.html')

@login_required
def index2(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(user=request.user, date__gte=today).order_by('date', 'start_time')
    expired_events = Event.objects.filter(user=request.user, date__lt=today).order_by('-date', '-start_time')
    return render(request, 'index2.html', {'upcoming_events': upcoming_events, 'expired_events': expired_events})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('index2')  # Redirect to the index page after event creation
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('index2')
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form, 'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('index2')
    return render(request, 'delete_event.html', {'event': event})
