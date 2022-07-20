import datetime
import secrets
import string

from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.http import HttpRequest
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

AGE_OR_GENDER_RESTRICTION = [
    ('18 Years And Above', '18 Years And Above'), ('Everyone', 'Everyone'),
    ('16 Years And Above', '16 Years And Above'), ('Males Only', 'Males Only'),
    ('Females Only', 'Females Only'),
]

TICKET_TYPE = [
    ('VVIP', 'VVIP'), ('VIP', 'VIP'), ('General', 'General')
]

EVENT_TYPE = [
    ('Concert', 'Concert'), ('Football Match', 'Football Match'), ('Movie', 'Movie'),
    ('Conference', 'Conference'), ('Seminar', 'Seminar'), ('Event', 'Event'),
]


class Event(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, default=1)
    event_type = models.CharField(max_length=100, choices=EVENT_TYPE, help_text='Type of Event e.g Concert.')
    name = models.CharField(max_length=50, verbose_name='Event Name',
                            help_text='The name of the Event must be descriptive and not misleading.')
    description = RichTextUploadingField()
    town = models.CharField(max_length=20)
    venue = models.CharField(max_length=30, help_text='Please specify the name of the place.')
    venue_location = models.CharField(max_length=50, help_text='Please paste the google maps coordinates', blank=True,
                                      null=True)
    organizer = models.CharField(max_length=30, verbose_name='Who is the Organizer of this Event?')
    banner_image = models.ImageField(upload_to='BannerImages', verbose_name='Upload a Banner Image for this Event')
    date_published = models.DateField(auto_now_add=True)
    date_starting = models.DateField(verbose_name='When is this Event starting?')
    time_starting = models.TimeField(verbose_name='At what time will this event start')
    date_ending = models.DateField(verbose_name='When will this Event close?')
    time_ending = models.TimeField(verbose_name='At what time will this Event close?')
    vvip_ticket_price = models.IntegerField(verbose_name='VVIP Ticket Price', blank=True, null=True)
    vip_ticket_price = models.IntegerField(verbose_name='VIP Ticket Price (Optional)',
                                           help_text='Price is in Zambian Kwacha (ZMW)', null=True, blank=True)
    general_ticket_price = models.IntegerField(verbose_name='General Ticket Price (Ordinary)',
                                               help_text='For events that have the General ticket setup.', blank=True, null=True)
    grand_stand_price = models.FloatField(blank=True, null=True)
    open_wing_price = models.FloatField(blank=True, null=True)
    west_wing_price = models.FloatField(blank=True, null=True)
    east_wing_price = models.FloatField(blank=True, null=True)
    north_wing_price = models.FloatField(blank=True, null=True)
    south_wing_price = models.FloatField(blank=True, null=True)
    lower_north_orange = models.FloatField(null=True, blank=True, verbose_name='Lower North (Orange)')
    upper_north_orange = models.FloatField(null=True, blank=True, verbose_name='Upper North (Orange)')
    upper_south_orange = models.FloatField(null=True, blank=True, verbose_name='Upper South (Orange)')
    lower_south_orange = models.FloatField(null=True, blank=True, verbose_name='Lower South (Orange)')
    upper_east_blue = models.FloatField(null=True, blank=True, verbose_name='Upper East Blue')
    lower_east_blue = models.FloatField(null=True, blank=True, verbose_name='Lower East Blue')
    west_wing_blue = models.FloatField(null=True, blank=True, verbose_name='West Wing (Blue)')
    children_price = models.FloatField(null=True, blank=True)
    sitting_plan = models.ImageField(upload_to='SittingPlans')
    age_or_gender_restriction = models.CharField(max_length=255, choices=AGE_OR_GENDER_RESTRICTION,
                                                 help_text='Who is Eligible to attend this Event?')
    additional_information = RichTextUploadingField()
    mobile_money_number = models.CharField(max_length=10,
                                           help_text='Mobile Money number where you want to receive funds for the '
                                                     'event.')

    class Meta:
        verbose_name_plural = 'My Events'

    def __str__(self):
        return self.name


class EventTicket(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, default=1)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_number = models.CharField(max_length=50, editable=False)
    type = models.CharField(max_length=20, choices=TICKET_TYPE)
    ticket_price = models.IntegerField(editable=False)
    datetime_bought = models.DateTimeField(auto_now_add=True)
    client_full_name = models.CharField(max_length=50)
    client_phone_number = models.CharField(max_length=14)
    scanned = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Events Tickets'

    def __str__(self):
        return self.ticket_number

    def save(self, *args, **kwargs):
        if self.type == 'VVIP':
            self.ticket_price = self.event.vvip_ticket_price
        elif self.type == 'VIP':
            self.ticket_price = self.event.vip_ticket_price
        elif self.type == 'General':
            self.ticket_price = self.event.general_ticket_price
        alphabet = string.ascii_uppercase + string.digits
        self.ticket_number = ''.join(secrets.choice(alphabet) for i in range(10))
        super(EventTicket, self).save(*args, **kwargs)


class All1ZedEventsCommission(models.Model):
    percentage_commission = models.IntegerField(default=8)

    def __str__(self):
        return f"{self.percentage_commission}% for every event ticket"

    class Meta:
        verbose_name_plural = 'All1Zed Events Commission'
        verbose_name = 'All1Zed Events Commission'


class SliderImage(models.Model):
    image = models.ImageField(verbose_name='Upload a slider image here')


from django.db import models


class KazangSession(models.Model):
    """
    Kazang (Content Ready Session).
    """
    session_uuid = models.CharField(max_length=255, editable=False)
    date_time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_uuid
