# Generated by Django 5.1.4 on 2024-12-29 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_edit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('video_file', models.FileField(upload_to='videos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='VideoEdit',
        ),
    ]
