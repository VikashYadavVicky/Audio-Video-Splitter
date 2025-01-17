from django.db import models

class SplitAudioUpload(models.Model):
    title = models.CharField(max_length=255)
    split_audio_file = models.FileField(upload_to='split_audios/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class SplitEquallyAudioUpload(models.Model):
    title = models.CharField(max_length=255)
    split_equally_audio_file = models.FileField(upload_to='split_equally_audios/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class MergeAudio(models.Model):
    merge_audios_files = models.ManyToManyField('UploadedFile', related_name='merge_audios')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Merge audio {self.id} - {self.uploaded_at}"

class UploadedFile(models.Model):
    file = models.FileField(upload_to='merge_audios/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name