# Generated by Django 5.1.4 on 2024-12-30 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_edit', '0006_extractaudio'),
    ]

    operations = [
        migrations.CreateModel(
            name='MergeVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merge_videos_file', models.FileField(upload_to='merge_videos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
