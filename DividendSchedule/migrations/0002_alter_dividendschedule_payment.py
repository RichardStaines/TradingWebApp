# Generated by Django 4.2.7 on 2023-11-16 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DividendSchedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dividendschedule',
            name='payment',
            field=models.DecimalField(decimal_places=6, max_digits=12),
        ),
    ]