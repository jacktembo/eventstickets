from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404,    get_list_or_404
from .models import Event, EventTicket
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
    popular_events = Event.objects.filter(date_starting__gte=today).annotate(Count('tickets')).order_by('-tickets__count')[:15]
    upcoming_events = Event.objects.filter(date_starting__gte=today).order_by('-date_starting')[:15]
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


def card_payment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'GET':
        client_phone_number = request.GET.get('client-phone-number')
        ticket_type = request.GET.get('ticket-type', False)
        client_full_name = request.GET.get('client-full-name', False)
        context = {
            'event_id': event_id, 'client_full_name': client_full_name,
            'ticket_type': ticket_type, 'client_phone_number': client_phone_number,
        }
        return render(request, 'payment_details.html', context)
    elif request.method == 'POST':
        ticket_type = request.POST.get('ticket-type', False)
        client_full_name = request.POST.get('client-full-name', False)
        client_phone_number = request.POST.get('client-phone-number')
        ticket = EventTicket(event=event, client_full_name=client_full_name, type=ticket_type, client_phone_number=client_phone_number)
        if ticket is not None:
            ticket.save()
            return HttpResponse('Thank you for your order!')
        else:
            return HttpResponse('Something went wrong!')