from time import timezone
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.urls import reverse

from .models import Event, EventTicket, SliderImage, All1ZedEventsCommission
from django.db.models import Avg, Count, Min, Sum
from datetime import datetime, date, timedelta, time
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django_xhtml2pdf.utils import pdf_decorator
import requests
import json
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from . import sms
from . import kazang
from . import phone_numbers
def index(request):
    """
    Featured events designates the four (4) featured events for a specific day or week or month.
    Featured events are those upcoming events with the highest number of tickets bought at a
    particular day or week.
    """
    today = date.today()
    slider_images = SliderImage.objects.all()
    first_slider_image = slider_images[0].image
    second_slider_image = slider_images[1].image
    third_slider_image = slider_images[2].image
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
        'slider_images': slider_images, 'first_slider_image': first_slider_image,
        'second_slider_image': second_slider_image, 'third_slider_image': third_slider_image,
    }
    return render(request, 'index.html', context)


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event': event,
    }
    return render(request, 'event_detail.html', context)


def mobile_payment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'GET':
        client_phone_number = request.GET.get('client-phone-number', False)
        ticket_type = request.GET.get('ticket-type', False)
        ticket_price = event.vvip_ticket_price if ticket_type == 'VVIP' else event.vip_ticket_price if ticket_type == 'VIP' else event.general_ticket_price if ticket_type == 'General' else None

        client_full_name = request.GET.get('client-full-name', False)
        context = {
            'event_id': event_id, 'client_full_name': client_full_name,
            'ticket_type': ticket_type, 'client_phone_number': client_phone_number,
            'ticket_price': ticket_price, 'event': event
        }
        return render(request, 'payment_details.html', context)

    elif request.method == 'POST':
        ticket_type = request.POST.get('ticket-type', False)
        ticket_price = event.vvip_ticket_price if ticket_type == 'VVIP' else event.vip_ticket_price if ticket_type == 'VIP' else event.general_ticket_price if ticket_type == 'General' else None
        charge = (float(ticket_price) * 100) + (0.02 * float(ticket_price) * 100)
        client_full_name = request.POST.get('client-full-name', False)
        client_phone_number = request.POST.get('client-phone-number')
        ticket = EventTicket(event=event, client_full_name=client_full_name,
                             type=ticket_type, user=event.user,
                             client_phone_number=client_phone_number)

        if phone_numbers.get_network(client_phone_number) == 'airtel':
            pay = kazang.airtel_pay_payment(client_phone_number, charge)
            context = {
                'ticket_type': ticket_type, 'client_full_name': client_full_name,
                'client_phone_number': client_phone_number, 'event_id': event_id,
                'ticket_price': ticket_price, 'event': event, 'reference_number': pay.get('airtel_reference', False)
            }
            return render(request, 'payment_waiting.html', context)
        elif phone_numbers.get_network(client_phone_number) == 'mtn':
            pass
        elif phone_numbers.get_network(client_phone_number) == 'zamtel':
            pass
        else:
            return HttpResponse('invalid phone nnumber')

def payment_approval(request, event_id):
    percentage_commission = All1ZedEventsCommission.objects.first().percentage_commission
    reference_number = request.POST.get('reference-number', False)
    event_id = request.POST.get('event_id', False)
    event = get_object_or_404(Event, pk=int(event_id))
    event_mobile_money_number = event.mobile_money_number
    ticket_type = request.POST.get('ticket-type', False)
    ticket_price = event.vvip_ticket_price if ticket_type == 'VVIP' else event.vip_ticket_price if ticket_type == 'VIP' else event.general_ticket_price if ticket_type == 'General' else None
    charge = (float(ticket_price) * 100) + (0.02 * float(ticket_price) * 100)
    client_full_name = request.POST.get('client-full-name', False)
    client_phone_number = request.POST.get('client-phone-number')
    ticket = EventTicket(event=event, client_full_name=client_full_name,
                         type=ticket_type, user=event.user,
                         client_phone_number=client_phone_number)
    ticket = EventTicket(event=event, client_full_name=client_full_name,
                         type=ticket_type, user=event.user,
                         client_phone_number=client_phone_number)
    if phone_numbers.get_network(client_phone_number) == 'airtel':
        r = kazang.airtel_pay_query(client_phone_number, charge, reference_number)
        if r.get('response_code', False) == '0':
            deposit = (float(ticket_price) * 100) - (float(ticket_price * 100) * (float(percentage_commission) / 100))
            if phone_numbers.get_network(event_mobile_money_number) == 'airtel':
                kazang.airtel_cash_in(event_mobile_money_number, deposit)
                ticket.save()
                message = f"Dear {client_full_name}, Your {event.name} Ticket Number is {ticket.ticket_number}. Download your ticket at https://events.all1zed.com/{ticket.ticket_number}/download. Thank you for using All1Zed Tickets."
                sms.send_sms(client_phone_number, message)
                context = {
                    'ticket_number': ticket.ticket_number, 'client_full_name': client_full_name,
                    'ticket_price': ticket_price, 'event': event
                }
                return render(request, 'payment_success.html', context)
            elif phone_numbers.get_network(event_mobile_money_number) == 'mtn':
                kazang.mtn_cash_in(event_mobile_money_number, deposit)
                ticket.save()
                message = f"Dear {client_full_name}, Your {event.name} Ticket Number is {ticket.ticket_number}. Download your ticket at https://events.all1zed.com/{ticket.ticket_number}/download. Thank you for using All1Zed Tickets."
                sms.send_sms(client_phone_number, message)
                context = {
                    'ticket_number': ticket.ticket_number, 'client_full_name': client_full_name,
                    'ticket_price': ticket_price, 'event': event
                }
                return render(request, 'payment_success.html', context)
            elif phone_numbers.get_network(event_mobile_money_number) == 'zamtel':
                kazang.zamtel_money_cash_in(event_mobile_money_number, deposit)
                ticket.save()
                message = f"Dear {client_full_name}, Your {event.name} Ticket Number is {ticket.ticket_number}. Download your ticket at https://events.all1zed.com/{ticket.ticket_number}/download. Thank you for using All1Zed Tickets."
                sms.send_sms(client_phone_number, message)
                context = {
                    'ticket_number': ticket.ticket_number, 'client_full_name': client_full_name,
                    'ticket_price': ticket_price, 'event': event
                }

                return render(request, 'payment_success.html', context)
            else:
                return HttpResponse('Event Owner phone number is invalid.')
        else:
            return HttpResponse(r['response_message'])


def generate_pdf_ticket(request):
    return render(request, 'ticket.html')


class DownloadView(WeasyTemplateResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        self.ticket_number = self.kwargs['ticket_number']
        ticket_number = self.ticket_number
        ticket = get_object_or_404(EventTicket, ticket_number=ticket_number)
        event = ticket.event
        qrcode_image = f'https://api.qrserver.com/v1/create-qr-code/?data={ticket_number}&size=200x200&format=svg'
        context = {
            'ticket': ticket, 'banner_image': event.banner_image, 'qrcode_image': qrcode_image,
            'event_name': ticket.event.name, 'ticket_number': ticket_number,
            'ticket_type': ticket.type, 'ticket_price': ticket.ticket_price,
            'city': ticket.event.town, 'venue': ticket.event.venue,
            'start_date': ticket.event.date_starting, 'end_date': ticket.event.date_ending,
            'start_time': ticket.event.time_starting.strftime("%H:%M hrs"), 'end_time': ticket.event.time_ending.strftime("%H:%M hrs"),
            'client_name': ticket.client_full_name, 'client_phone_number': ticket.client_phone_number,

        }
        return context

    template_name = 'ticket.html'

    def get_pdf_filename(self):
        return 'All1Zed-ticket-{at}.pdf'



def scan(request):
    return render(request, 'qrcode_scanner_instascan.html')


def tickets_list(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    tickets = get_list_or_404(EventTicket, event=event)
    context = {
        'tickets': tickets, 'event': event,
    }
    return render(request, 'tickets_list.html', context)


class TicketsListView(WeasyTemplateResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        self.event_id = self.kwargs['event_id']
        event = get_object_or_404(Event, pk=self.event_id)
        tickets = get_list_or_404(EventTicket, event=event)
        context = {
            'tickets': tickets, 'event': event,
        }
        return context

    template_name = 'tickets_list.html'


def scan_ticket(request, ticket_number):
    ticket = EventTicket.objects.filter(ticket_number=ticket_number)
    if ticket.exists() and not ticket.first().scanned:
        ticket.update(scanned=True)
        return JsonResponse('Verified Successfully', safe=False)
    elif ticket.exists() and ticket.first().scanned:
        return JsonResponse('Ticket Already Scanned', safe=False)
    else:
        return JsonResponse('Invalid Ticket', safe=False)


def events(request):
    events = Event.objects.all()
    paginator = Paginator(events, 20)
    page_number = request.GET.get('page')
    events_page_object = paginator.get_page(page_number)
    context = {
        'events': events, 'page_number': page_number, 'paginator': paginator,
        'page_obj': events_page_object,
    }
    return render(request, 'events.html', context)


def payment_waiting(request):
    return render(request, 'payment_waiting.html')


# def pay(request, event):
#     phone_number = request.POST.get('client-phone-number', False)
#     full_name = request.POST.get('client-full-name', False)
#     event = Event.objects.get(id=int(request.POST.get('event-id', False)))
#     amount = str(int(Event.objects.get(id=int(request.data['route'])).price * 100))
#     if phone_numbers.get_network(phone_number) == 'airtel':
#         r = kazang.airtel_pay_payment(phone_number, amount)
#         context = {
#             'reference_number': r['reference_number']
#         }
#         return render('payment_waiting.html', context)
#     elif phone_numbers.get_network(phone_number) == 'zamtel':
#         r = kazang.zamtel_money_pay(phone_number, amount)
#         return Response({'reference_number': r['confirmation_number']})
#     elif phone_numbers.get_network(phone_number) == 'mtn':
#         r = kazang.mtn_debit(phone_number, amount)
#         return Response({'reference_number': r.get('supplier_transaction_id', r)})


# def pay_confirm(request):
#     phone_number = request.data['passenger_phone']
#     amount = str(int(Route.objects.get(id=int(request.data['route'])).price * 100))
#     reference_number = request.data['reference_number']
#     passenger_first_name = request.data.get('passenger_first_name', None)
#     passenger_last_name = request.data.get('passenger_last_name', None)
#     passenger_phone = phone_number
#     departure_date = date.fromisoformat(request.data['departure_date'])
#     route = Route.objects.get(id=int(request.data.get('route', None)))
#     seat_number = request.data.get('seat_number', None)
#     ticket = Ticket.objects.create(passenger_phone=passenger_phone, passenger_first_name=passenger_first_name,
#                                    passenger_last_name=passenger_last_name, departure_date=departure_date,
#                                    route=route, seat_number=int(seat_number)
#                                    )
#     serializer = TicketSerializer(ticket)
#     if phone_numbers.get_network(phone_number) == 'airtel':  # If the number is airtel, process accordingly.
#         confirm = kazang.airtel_pay_query(phone_number, amount, reference_number)
#         if not confirm.get('response_code', False) == 0:
#             return Response({"message": "success", "ticket": serializer.data,
#                              "ticket_url": f"https://all1zed-tickets.herokuapp.com/api/tickets/{ticket.ticket_number}"})
#         else:
#             return Response(
#                 {"message": "declined", "reason": "customer has not yet approved the funds for the ticket."},
#                 status=status.HTTP_402_PAYMENT_REQUIRED)
#
#     elif phone_numbers.get_network(phone_number) == 'zamtel':
#         confirm = kazang.zamtel_money_pay_confirm(phone_number, amount, reference_number)
#         if confirm.get('response_code', False) == 0:
#             return Response({"message": "success", "ticket": serializer.data,
#                              "ticket_url": f"https://all1zed-tickets.herokuapp.com/api/tickets/{ticket.ticket_number}"})
#         else:
#             return Response(
#                 {"message": "declined", "reason": "customer has not yet approved the funds for the ticket."},
#                 status=status.HTTP_402_PAYMENT_REQUIRED)
#
#     elif phone_numbers.get_network(phone_number) == 'mtn':
#         pass

