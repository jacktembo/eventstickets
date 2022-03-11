from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404,    get_list_or_404
from .models import Event
from django.db.models import Avg, Count, Min, Sum
from datetime import datetime, date, timedelta, time
from django.core.paginator import Paginator


def index(request):
    """
    Featured events designates the four (4) featured events for a specific day or week or month.
    Featured events are those upcoming events with the highest number of tickets bought at a
    particular day or week.
    """
    today = date.today()
    popular_events = Event.objects.filter(date_starting__gte=today).annotate(Count('tickets')).order_by('-tickets__count')[:20]
    upcoming_events = Event.objects.filter(date_starting__gte=today).order_by('-date_starting')[:20]
    popular_event_paginator = Paginator(popular_events, 16)
    upcoming_events_paginator = Paginator(upcoming_events, 16)
    context = {
        'upcoming_events': upcoming_events, 'popular_events': popular_events,
        'popular_events_paginator': popular_event_paginator,
        'upcoming_events_paginator': upcoming_events_paginator,
    }
    return render(request, 'index.html', context)


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event': event,
    }
    return render(request, 'event_detail.html', context)
