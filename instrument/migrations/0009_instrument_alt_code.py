# Generated by Django 4.2.7 on 2023-11-30 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrument', '0008_alter_instrument_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='alt_code',
            field=models.CharField(default='', max_length=10),
        ),
    ]