# Generated by Django 5.0.6 on 2024-07-16 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0032_remove_presentationparams_orienting_rotation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='thumbnail_contenttype',
            field=models.CharField(blank=True, null=True),
        ),
    ]