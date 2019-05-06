# Generated by Django 2.0.7 on 2019-05-03 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0054_careplanvitaltemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitaltask',
            name='vital_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vital_tasks', to='tasks.CarePlanVitalTemplate'),
        ),
    ]
