# Generated by Django 4.2.7 on 2023-11-10 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dividends', '0003_rename_portfolio_id_dividend_portfolio'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='dividend',
            table='app_dividend',
        ),
    ]
