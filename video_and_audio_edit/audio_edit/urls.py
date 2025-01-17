from django.urls import path
from . import views

app_name = 'audio_edit'

urlpatterns = [
    path('', views.audio_tools, name='audio_tools'),
     
    # split audio
    path('upload-audio/', views.upload_audio_and_split, name='upload_audio_and_split'),
    
    # split equally chacker
    path('split-audio-equally/', views.split_audio_equally, name='split_audio_equally'),
    path('download_all_clips/', views.download_all_clips, name='download_all_clips'),
    
    # Marge audio 
    path('upload-and-merge-audio/', views.upload_and_merge_audio, name='upload_and_merge_audio'),
]