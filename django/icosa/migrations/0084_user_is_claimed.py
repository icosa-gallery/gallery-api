# Generated by Django 5.0.6 on 2024-12-11 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0083_asset_triangle_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_claimed',
            field=models.BooleanField(default=True),
        ),
    ]