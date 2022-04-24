# Generated by Django 4.0.4 on 2022-04-23 00:41

from django.db import migrations
import django_google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_alter_event_venue_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='address',
            field=django_google_maps.fields.AddressField(default='Jaaa', max_length=200),
            preserve_default=False,
        ),
    ]