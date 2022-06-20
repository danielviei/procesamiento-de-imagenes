# Generated by Django 4.0.5 on 2022-06-19 21:59

from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_jobs_status_alter_steps_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageTransformationFSM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', django_fsm.FSMField(default=1, max_length=50)),
                ('image_path', models.FilePathField()),
                ('extension', models.CharField(max_length=5)),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.jobs')),
            ],
        ),
    ]
