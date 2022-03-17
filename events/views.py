import math
from time import timezone

from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, get_list_or_404
from .models import Event, EventTicket
from django.db.models import Avg, Count, Min, Sum
from datetime import datetime, date, timedelta, time
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django_xhtml2pdf.utils import pdf_decorator
import requests
import json
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse


def send_sms(recipient, message):
    url = "https://probasesms.com/api/json/multi/res/bulk/sms"
    payload = json.dumps({
        "username": "All1Zed@12$$", "password": "All1Zed@sms12$$",
        "recipient": [int('26' + recipient)], "senderid": "All1Zed", "message": message,
        "source": "All1Zed"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code


def index(request):
    """
    Featured events designates the four (4) featured events for a specific day or week or month.
    Featured events are those upcoming events with the highest number of tickets bought at a
    particular day or week.
    """
    today = date.today()
    popular_events = Event.objects.filter(date_starting__gte=today).annotate(Count('tickets')).order_by(
        '-tickets__count')
    upcoming_events = Event.objects.filter(date_starting__gte=today).order_by('date_starting')
    popular_events_paginator = Paginator(popular_events, 16)
    upcoming_events_paginator = Paginator(upcoming_events, 16)
    page_number = request.GET.get('page')
    # upcoming_page = upcoming_events_paginator.page(page_number)
    # popular_page = popular_events_paginator.page(page_number)
    upcoming_page_obj = upcoming_events_paginator.get_page(page_number)
    popular_page_obj = popular_events_paginator.get_page(page_number)

    context = {
        'upcoming_events': upcoming_events, 'popular_events': popular_events,
        'popular_events_paginator': popular_events_paginator,
        'upcoming_events_paginator': upcoming_events_paginator, 'page_number': page_number,
        'upcoming_page_obj': upcoming_page_obj, 'popular_page_obj': popular_page_obj,
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
        client_phone_number = request.GET.get('client-phone-number', False)
        ticket_type = request.GET.get('ticket-type', False)
        ticket_price = event.vvip_ticket_price if ticket_type == 'VVIP' else event.vip_ticket_price if ticket_type == 'VIP' else event.general_ticket_price if ticket_type == 'General' else None

        client_full_name = request.GET.get('client-full-name', False)
        context = {
            'event_id': event_id, 'client_full_name': client_full_name,
            'ticket_type': ticket_type, 'client_phone_number': client_phone_number,
            'ticket_price': ticket_price,
        }
        return render(request, 'payment_details.html', context)
    elif request.method == 'POST':
        ticket_type = request.POST.get('ticket-type', False)
        client_full_name = request.POST.get('client-full-name', False)
        client_phone_number = request.POST.get('client-phone-number')
        ticket = EventTicket(event=event, client_full_name=client_full_name,
                             type=ticket_type, user=event.user,
                             client_phone_number=client_phone_number)
        if 1 < 5:
            assert ticket.client_full_name != False and ticket.client_phone_number != False \
                   and ticket.type != False
            ticket.save()
            message = f'Dear {ticket.client_full_name}. Your All1Zed Ticket Number is {ticket.ticket_number}. Download your Ticket at ' \
                      f'https://all1zed.com.'
            send_sms(
                ticket.client_phone_number, message
            )
            return HttpResponse(f'your ticket number is {ticket.ticket_number}')
        else:
            return HttpResponse('Something went wrong!')


# @pdf_decorator()
def generate_pdf_ticket(request):
    return render(request, 'ticket.html')


class DownloadView(WeasyTemplateResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        self.ticket_number = self.kwargs['ticket_number']
        ticket_number = self.ticket_number
        ticket = get_object_or_404(EventTicket, ticket_number=ticket_number)
        event = ticket.event
        context = {
            'ticket': ticket,
            'event_name': ticket.event.name, 'ticket_number': ticket_number,
            'ticket_type': ticket.type, 'ticket_price': ticket.ticket_price,
            'city': ticket.event.town, 'venue': ticket.event.venue,
            'start_date': ticket.event.date_starting, 'end_date': ticket.event.date_ending,
            'start_time': ticket.event.time_starting.strftime("%H:%M hrs"), 'end_time': ticket.event.time_ending.strftime("%H:%M hrs"),
            'client_name': ticket.client_full_name, 'client_phone_number': ticket.client_phone_number,

        }
        return context

    template_name = 'ticket.html'

    # extra_context = {
    #     'client_name': 'j'
    # }
    # dynamically generate filename

    def get_pdf_filename(self):
        return 'All1Zed-ticket-{at}.pdf'
