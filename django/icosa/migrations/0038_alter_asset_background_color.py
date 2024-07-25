# Generated by Django 5.0.6 on 2024-07-25 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0037_user_access_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='background_color',
            field=models.CharField(blank=True, help_text='A valid css colour, such as #00CC83', max_length=7, null=True),
        ),
    ]
