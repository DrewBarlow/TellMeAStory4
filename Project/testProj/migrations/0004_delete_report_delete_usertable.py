# Generated by Django 4.0.3 on 2022-04-01 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testProj', '0003_alter_report_report_reason'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Report',
        ),
        migrations.DeleteModel(
            name='UserTable',
        ),
    ]
