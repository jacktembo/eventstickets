# Generated by Django 4.0.2 on 2022-03-09 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='town',
            field=models.CharField(default='Lusaka', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='eventticket',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='events.event'),
        ),
    ]
