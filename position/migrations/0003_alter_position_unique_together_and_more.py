# Generated by Django 4.2.7 on 2023-11-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_portfolio_table'),
        ('instrument', '0005_alter_instrument_company_link_and_more'),
        ('position', '0002_alter_position_quantity'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='position',
            unique_together={('portfolio', 'instrument')},
        ),
        migrations.AddIndex(
            model_name='position',
            index=models.Index(fields=['portfolio', 'instrument'], name='app_positio_portfol_26e598_idx'),
        ),
    ]
