# Generated by Django 5.0.6 on 2024-06-12 13:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("icosa", "0004_auto_20240612_1303"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="color_space",
            field=models.CharField(
                choices=[("LINEAR", "LINEAR"), ("GAMMA", "GAMMA")],
                default="GAMMA",
                max_length=50,
            ),
        ),
    ]