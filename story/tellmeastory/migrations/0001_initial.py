# Generated by Django 4.0.4 on 2022-05-12 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('managetags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bannedUser', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, upload_to='storyimages')),
                ('post_id', models.CharField(default='', max_length=200)),
                ('image_url', models.TextField()),
                ('node_title', models.CharField(max_length=200)),
                ('node_content', models.CharField(max_length=10000)),
                ('has_image_file', models.BooleanField(default=False)),
                ('longitude', models.DecimalField(decimal_places=21, max_digits=25, null=True)),
                ('latitude', models.DecimalField(decimal_places=21, max_digits=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=512)),
                ('display_name', models.CharField(max_length=200)),
                ('mature', models.BooleanField(default=False)),
                ('user_blurb', models.CharField(default='', max_length=1000)),
                ('admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_reason', models.CharField(max_length=600)),
                ('id_for_report', models.CharField(default='', max_length=100)),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tellmeastory.node')),
                ('reported_user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reported_user', to='tellmeastory.user')),
                ('reporting_username', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_reporting', to='tellmeastory.user')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emoji', models.CharField(max_length=1)),
                ('node', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tellmeastory.node')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tellmeastory.user')),
            ],
        ),
        migrations.AddField(
            model_name='node',
            name='node_author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tellmeastory.user'),
        ),
        migrations.AddField(
            model_name='node',
            name='other_tags',
            field=models.ManyToManyField(blank=True, to='managetags.tag'),
        ),
    ]
