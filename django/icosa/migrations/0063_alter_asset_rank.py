# Generated by Django 5.0.6 on 2024-09-13 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0062_asset_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='rank',
            field=models.FloatField(default=0),
        ),
    ]