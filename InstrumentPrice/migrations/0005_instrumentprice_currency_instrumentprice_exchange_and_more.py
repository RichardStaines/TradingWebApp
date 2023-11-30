# Generated by Django 4.2.7 on 2023-11-30 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InstrumentPrice', '0004_instrumentprice_ma200_instrumentprice_ma50_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrumentprice',
            name='currency',
            field=models.CharField(default='', max_length=4),
        ),
        migrations.AddField(
            model_name='instrumentprice',
            name='exchange',
            field=models.CharField(default='', max_length=6),
        ),
        migrations.AddField(
            model_name='instrumentprice',
            name='mkt_cap',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
