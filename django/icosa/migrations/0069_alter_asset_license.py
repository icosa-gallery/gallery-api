# Generated by Django 5.0.6 on 2024-10-29 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0068_rename_camera_transform_asset_camera'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='license',
            field=models.CharField(blank=True, choices=[('', 'Please choose'), ('CREATIVE_COMMONS_BY_4_0', 'CC BY Attribution 4.0 International'), ('CREATIVE_COMMONS_BY_ND_4_0', 'CC BY-ND Attribution-NoDerivatives 4.0 International'), ('CREATIVE_COMMONS_0', 'CC0 1.0 Universal'), ('ALL_RIGHTS_RESERVED', 'All rights reserved')], max_length=50, null=True),
        ),
    ]
