# Generated by Django 5.0.6 on 2024-06-25 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0011_tag_remove_asset_tags_asset_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
