# Generated by Django 4.0.3 on 2022-04-28 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tellmeastory', '0006_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='username',
            field=models.CharField(default='Giads123', max_length=200),
        ),
    ]
