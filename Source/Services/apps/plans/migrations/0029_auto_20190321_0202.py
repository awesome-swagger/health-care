# Generated by Django 2.0.7 on 2019-03-21 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0028_auto_20190307_0946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='careplan',
            options={'ordering': ('patient', 'plan_template')},
        ),
        migrations.AlterModelOptions(
            name='careplantemplate',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='planconsent',
            options={'ordering': ('plan',)},
        ),
    ]
