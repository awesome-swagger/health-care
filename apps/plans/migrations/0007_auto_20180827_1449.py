# Generated by Django 2.0.7 on 2018-08-27 20:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0006_auto_20180817_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoMessage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(blank=True, max_length=512, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InfoMessageQueue',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('type', models.CharField(choices=[('education', 'Education'), ('support', 'Support'), ('medication', 'Medication')], max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='streammessage',
            name='stream',
        ),
        migrations.RemoveField(
            model_name='careplantemplate',
            name='goals',
        ),
        migrations.RemoveField(
            model_name='careplantemplate',
            name='message_streams',
        ),
        migrations.RemoveField(
            model_name='careplantemplate',
            name='team_tasks',
        ),
        migrations.AddField(
            model_name='goal',
            name='plan_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='plans.CarePlanTemplate'),
        ),
        migrations.AddField(
            model_name='patienttask',
            name='plan_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_tasks', to='plans.CarePlanTemplate'),
        ),
        migrations.AddField(
            model_name='teamtask',
            name='plan_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_tasks', to='plans.CarePlanTemplate'),
        ),
        migrations.AlterField(
            model_name='careplaninstance',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='care_plans', to='patients.PatientProfile'),
        ),
        migrations.DeleteModel(
            name='MessageStream',
        ),
        migrations.DeleteModel(
            name='StreamMessage',
        ),
        migrations.AddField(
            model_name='infomessagequeue',
            name='plan_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info_message_queues', to='plans.CarePlanTemplate'),
        ),
        migrations.AddField(
            model_name='infomessage',
            name='queue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='plans.InfoMessageQueue'),
        ),
    ]