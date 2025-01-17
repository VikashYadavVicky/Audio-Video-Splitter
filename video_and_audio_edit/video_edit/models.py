from django.db import models

class SplitVideoUpload(models.Model):
    title = models.CharField(max_length=255)
    split_video_file = models.FileField(upload_to='split_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class SplitEquallyVideoUpload(models.Model):
    title = models.CharField(max_length=255)
    split_equally_video_file = models.FileField(upload_to='split_equally_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ExtractAudio(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='videos_for_audio/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class MergeVideo(models.Model):
    merge_videos_files = models.ManyToManyField('UploadedFile', related_name='merge_videos')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Merge Video {self.id} - {self.uploaded_at}"

class UploadedFile(models.Model):
    file = models.FileField(upload_to='merge_videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name