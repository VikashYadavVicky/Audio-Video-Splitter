from django.urls import path
from . import views

app_name = 'video_edit'

urlpatterns = [
    path('', views.video_tools, name='video_tools'),
       
    # Split
    path('upload-video/', views.upload_video_and_split, name='upload_video_and_split'),
    
    # split equally chacker
    path('split_video_equally/', views.split_video_equally, name='split_video_equally'),
    path('download_all_clips/', views.download_all_clips, name='download_all_clips'),
    
    
    # Extract audio urls
    path('upload-video-and-extract-audio/', views.upload_video_and_extract_audio, name='upload_video_and_extract_audio'),
    
    # merge video urls
    path('upload-and-merge-videos/', views.upload_and_merge_videos, name='upload_and_merge_videos'),
    
]