# Generated by Django 4.2.7 on 2023-11-29 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_portfolio_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='portfolio',
            options={'ordering': ('name',)},
        ),
    ]