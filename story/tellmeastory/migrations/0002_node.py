# Generated by Django 4.0.3 on 2022-04-12 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tellmeastory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='storyimages')),
                ('node_title', models.CharField(max_length=200)),
                ('node_content', models.CharField(max_length=10000)),
                ('node_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tellmeastory.user')),
            ],
        ),
    ]
