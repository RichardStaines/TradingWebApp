# Generated by Django 4.2.7 on 2023-11-08 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dividends', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dividend',
            name='payment_date',
            field=models.DateField(),
        ),
    ]
