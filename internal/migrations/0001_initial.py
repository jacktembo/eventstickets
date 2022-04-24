# Generated by Django 4.0.4 on 2022-04-22 15:32

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TermsAndConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_terms_and_conditions', ckeditor_uploader.fields.RichTextUploadingField()),
                ('event_organizer_terms_and_conditions', ckeditor_uploader.fields.RichTextUploadingField()),
                ('privacy_policy', ckeditor_uploader.fields.RichTextUploadingField()),
                ('terms_of_use', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
            options={
                'verbose_name': 'Terms And Conditions',
                'verbose_name_plural': 'Terms And Conditions',
            },
        ),
    ]