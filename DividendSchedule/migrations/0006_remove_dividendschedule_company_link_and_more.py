# Generated by Django 4.2.7 on 2023-11-16 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DividendSchedule', '0005_rename_external_link2_dividendschedule_company_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dividendschedule',
            name='company_link',
        ),
        migrations.RemoveField(
            model_name='dividendschedule',
            name='external_link',
        ),
    ]
