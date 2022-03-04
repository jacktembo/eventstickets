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


class Event(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    name = models.CharField(max_length=50, verbose_name='Event Name',
                            help_text='The name of the Event must be descriptive and not misleading.')
    description = RichTextUploadingField()
    venue = models.CharField(max_length=255, help_text='Please specify the name of the place.')
    venue_location = models.CharField(max_length=50, help_text='Please paste the google maps coordinates', blank=True,
                                      null=True)
    organizer = models.CharField(max_length=255, verbose_name='Who is the Organizer of this Event?')
    banner_image = models.ImageField(upload_to='events/images', verbose_name='Upload a Banner Image for this Event',
                                     blank=True, null=True)
    date_time_published = models.DateTimeField(auto_now_add=True)
    date_starting = models.DateField(verbose_name='When is this Event starting?')
    time_starting = models.TimeField(verbose_name='At what time will this event start')
    date_ending = models.DateField(verbose_name='When will this Event close?')
    time_ending = models.TimeField(verbose_name='At what time will this Event close?')
    vvip_ticket_price = models.IntegerField(verbose_name='VVIP Ticket Price')
    vip_ticket_price = models.IntegerField(verbose_name='VIP Ticket Price',
                                           help_text='Price is in Zambian Kwacha (ZMW)')
    general_ticket_price = models.IntegerField(verbose_name='General Ticket Price (Ordinary)',
                                               help_text='Price is in Zambian Kwacha (ZMW)')
    sitting_plan = models.FileField(blank=True, null=True)
    age_or_gender_restriction = models.CharField(max_length=255, choices=AGE_OR_GENDER_RESTRICTION,
                                                 help_text='Who is Eligible to attend this Event?')
    additional_information = RichTextUploadingField()

    class Meta:
        verbose_name_plural = 'My Events'

    def __str__(self):
        return self.name


class EventTicket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=TICKET_TYPE)
    ticket_price = models.IntegerField(editable=False)
    datetime_bought = models.DateTimeField(auto_now_add=True)
    client_first_name = models.CharField(max_length=50)
    client_last_name = models.CharField(max_length=50)

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
        super(EventTicket, self).save(*args, **kwargs)


class All1ZedEventsCommission(models.Model):
    percentage_commission = models.IntegerField(default=8)

    def __str__(self):
        return f"{self.percentage_commission}% for every event ticket"

    class Meta:
        verbose_name_plural = 'All1Zed Events Commission'
        verbose_name = 'All1Zed Events Commission'
