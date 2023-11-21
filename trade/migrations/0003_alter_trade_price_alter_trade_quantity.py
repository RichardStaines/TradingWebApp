# Generated by Django 4.2.7 on 2023-11-21 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_alter_trade_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='price',
            field=models.DecimalField(decimal_places=6, max_digits=12),
        ),
        migrations.AlterField(
            model_name='trade',
            name='quantity',
            field=models.DecimalField(decimal_places=0, max_digits=12),
        ),
    ]