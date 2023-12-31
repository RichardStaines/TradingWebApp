# Generated by Django 4.2.7 on 2023-11-20 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('portfolio', '0002_alter_portfolio_table'),
        ('instrument', '0005_alter_instrument_company_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=12)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('avg_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('notes', models.CharField(max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instrument.instrument')),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfolio')),
            ],
            options={
                'db_table': 'app_position',
            },
        ),
    ]
