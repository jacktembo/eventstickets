# Generated by Django 4.0.4 on 2022-07-22 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_general_ticket_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='vip_orange',
            field=models.FloatField(blank=True, null=True, verbose_name='VIP (orange)'),
        ),
        migrations.AddField(
            model_name='event',
            name='vip_red',
            field=models.FloatField(blank=True, null=True, verbose_name='VIP (Red)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='general_ticket_price',
            field=models.FloatField(blank=True, help_text='For events that have the General ticket setup.', null=True, verbose_name='General Ticket Price (Ordinary)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='lower_east_blue',
            field=models.FloatField(blank=True, null=True, verbose_name='Lower East (Blue) Price'),
        ),
        migrations.AlterField(
            model_name='event',
            name='lower_north_orange',
            field=models.FloatField(blank=True, null=True, verbose_name='Lower North (Orange) Price'),
        ),
        migrations.AlterField(
            model_name='event',
            name='lower_south_orange',
            field=models.FloatField(blank=True, null=True, verbose_name='Lower South (Orange) Price'),
        ),
        migrations.AlterField(
            model_name='event',
            name='upper_east_blue',
            field=models.FloatField(blank=True, null=True, verbose_name='Upper East (Blue) Price'),
        ),
        migrations.AlterField(
            model_name='event',
            name='upper_north_orange',
            field=models.FloatField(blank=True, null=True, verbose_name='Upper North (Orange) Price'),
        ),
        migrations.AlterField(
            model_name='event',
            name='upper_south_orange',
            field=models.FloatField(blank=True, null=True, verbose_name='Upper South (Orange) Price'),
        ),
        migrations.AlterField(
            model_name='event',
            name='vip_ticket_price',
            field=models.FloatField(blank=True, help_text='Price is in Zambian Kwacha (ZMW)', null=True, verbose_name='VIP Ticket Price'),
        ),
        migrations.AlterField(
            model_name='event',
            name='vvip_ticket_price',
            field=models.FloatField(blank=True, null=True, verbose_name='VVIP Ticket Price'),
        ),
        migrations.AlterField(
            model_name='event',
            name='west_wing_blue',
            field=models.FloatField(blank=True, null=True, verbose_name='West Wing (Blue) Price'),
        ),
    ]
