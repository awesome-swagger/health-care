# Generated by Django 2.0.7 on 2019-06-27 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0013_auto_20190610_0059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billedactivity',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='billedactivity',
            name='team_task_template',
        ),
    ]
