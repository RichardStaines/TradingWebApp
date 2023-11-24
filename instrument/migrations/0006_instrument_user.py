# Generated by Django 4.2.7 on 2023-11-24 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instrument', '0005_alter_instrument_company_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
