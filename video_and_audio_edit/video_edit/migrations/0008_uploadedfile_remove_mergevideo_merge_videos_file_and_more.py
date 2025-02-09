# Generated by Django 5.1.4 on 2024-12-30 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_edit', '0007_mergevideo'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='merge_videos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='mergevideo',
            name='merge_videos_file',
        ),
        migrations.AddField(
            model_name='mergevideo',
            name='merge_videos_files',
            field=models.ManyToManyField(related_name='merge_videos', to='video_edit.uploadedfile'),
        ),
    ]
