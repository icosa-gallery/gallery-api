# Generated by Django 5.0.6 on 2024-06-26 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0016_alter_asset_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='IcosaFormat',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=255)),
                ('format', models.CharField(max_length=255)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icosa.asset')),
                ('subfiles', models.ManyToManyField(blank=True, related_name='parent_files', to='icosa.icosaformat')),
            ],
        ),
    ]
