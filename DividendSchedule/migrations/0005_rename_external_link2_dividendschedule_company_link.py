# Generated by Django 4.2.7 on 2023-11-16 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DividendSchedule', '0004_dividendschedule_external_link2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dividendschedule',
            old_name='external_link2',
            new_name='company_link',
        ),
    ]
