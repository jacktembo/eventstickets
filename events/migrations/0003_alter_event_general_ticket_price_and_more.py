# Generated by Django 4.0.4 on 2022-07-20 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_children_price_event_east_wing_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='general_ticket_price',
            field=models.IntegerField(blank=True, help_text='Price is in Zambian Kwacha (ZMW)', null=True, verbose_name='General Ticket Price (Ordinary)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='vip_ticket_price',
            field=models.IntegerField(blank=True, help_text='Price is in Zambian Kwacha (ZMW)', null=True, verbose_name='VIP Ticket Price (Optional)'),
        ),
    ]
