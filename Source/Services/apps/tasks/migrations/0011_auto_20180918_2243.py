# Generated by Django 2.0.7 on 2018-09-19 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_merge_20180918_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmenttask',
            name='comments',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='symptomtask',
            name='comments',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]