# Generated by Django 4.0.5 on 2022-06-19 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_imagetransformationfsm'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagetransformationfsm',
            name='current_image',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]