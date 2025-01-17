from django.contrib import admin
from .models import SplitAudioUpload,SplitEquallyAudioUpload,MergeAudio
# Register your models here.

@admin.register(SplitAudioUpload)
class SplitAudioAdmin(admin.ModelAdmin):
    list_display=['id','title','split_audio_file','uploaded_at']
    
@admin.register(SplitEquallyAudioUpload)
class SplitEquallyAudioAdmin(admin.ModelAdmin):
    list_display=['id','title','split_equally_audio_file','uploaded_at']
        
    
# @admin.register(MergeAudio)
# class MergeAudioAdmin(admin.ModelAdmin):
#     list_display=['id','merge_Audios_file','uploaded_at']