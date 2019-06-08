# Generated by Django 2.0.7 on 2019-06-08 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0073_remove_vitalquestion_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symptomtask',
            name='symptom_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symptom_tasks', to='tasks.CarePlanSymptomTemplate'),
        ),
    ]
