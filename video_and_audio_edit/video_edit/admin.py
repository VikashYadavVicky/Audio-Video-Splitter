from django.contrib import admin
from .models import SplitVideoUpload,SplitEquallyVideoUpload,ExtractAudio,MergeVideo
# Register your models here.

@admin.register(SplitVideoUpload)
class SplitVideoAdmin(admin.ModelAdmin):
    list_display=['id','title','split_video_file','uploaded_at']
    
@admin.register(SplitEquallyVideoUpload)
class SplitEquallyVideoAdmin(admin.ModelAdmin):
    list_display=['id','title','split_equally_video_file','uploaded_at']
    
@admin.register(ExtractAudio)
class ExtractAudioAdmin(admin.ModelAdmin):
    list_display=['id','title','audio_file','uploaded_at']
    
    
# @admin.register(MergeVideo)
# class MergeVideoAdmin(admin.ModelAdmin):
#     list_display=['id','merge_videos_file','uploaded_at']