# Generated by Django 5.0.6 on 2024-11-07 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icosa', '0079_hiddenmediafilelog_deleted_from_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='state',
            field=models.CharField(choices=[('BARE', 'Bare'), ('UPLOADING', 'Uploading'), ('COMPLETE', 'Complete'), ('FAILED', 'Failed')], db_default='BARE', default='BARE', max_length=255),
        ),
    ]