# Generated by Django 4.0.5 on 2022-06-20 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_alter_jobs_options_alter_jobs_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='step',
            field=models.IntegerField(null=True),
        ),
    ]