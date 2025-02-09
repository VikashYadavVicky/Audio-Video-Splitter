# Generated by Django 5.1.4 on 2024-12-29 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_edit', '0002_videoupload_delete_videoedit'),
    ]

    operations = [
        migrations.CreateModel(
            name='SplitEquallyVideoUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('split_equally_video_file', models.FileField(upload_to='split_equally_videos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SplitVideoUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('split_video_file', models.FileField(upload_to='split_videos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='VideoUpload',
        ),
    ]
