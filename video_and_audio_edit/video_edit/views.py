
import os
import tempfile   
from moviepy import VideoFileClip,concatenate_videoclips
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.shortcuts import render


def video_tools(request):
    return render(request, 'video_edit/video_tools/video_tools.html')


# **********************Split video Section**************************


def upload_video_and_split(request):
    if request.method == 'POST' and request.FILES.get('video_file'):

        uploaded_file = request.FILES['video_file']
        
        temp_dir = tempfile.mkdtemp()
        temp_video_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_video_path, 'wb') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
 
        start_time = int(request.POST.get('start_time', 0)) 
        end_time = int(request.POST.get('end_time', 0))  

        clip = VideoFileClip(temp_video_path)
        total_duration = clip.duration

        if end_time == 0 or end_time > total_duration:
            end_time = total_duration  
        
        if start_time >= end_time:
            return HttpResponse("Invalid start and end times. Start time must be less than end time.")

        sliced_clip = clip.subclipped(start_time, end_time)

        sliced_file_name = "sliced_video.mp4"
        sliced_file_path = os.path.join(settings.MEDIA_ROOT, "split_clips", sliced_file_name)
        sliced_clip.write_videofile(sliced_file_path)
        
        clip.close()
        sliced_clip.close()

        sliced_video_url = os.path.join(settings.MEDIA_URL, "split_clips", sliced_file_name)
        
        return render(request, 'video_edit/split_video_page.html', {
            'sliced_video_url': sliced_video_url
        })

    return render(request, 'video_edit/split_video_page.html')



# **********************Split video Equally Section**************************


def split_video_equally(request):
    if request.method == 'POST' and request.FILES.get('video_file'):
        uploaded_file = request.FILES['video_file']

        if not uploaded_file.name.endswith(('.mp4')):
            return HttpResponse("Unsupported file format. Please upload a valid video file.")

        temp_dir = tempfile.mkdtemp()
        temp_video_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_video_path, 'wb') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        try:
            video_clip = VideoFileClip(temp_video_path)
            video_duration = video_clip.duration
        except Exception as e:
            return HttpResponse(f"Error loading video file: {str(e)}")
        
        clip_duration = int(request.POST.get('clip_time', 0))
        end_time = clip_duration

        if clip_duration <= 0:
            return HttpResponse("Clip duration must be greater than 0.")
        elif clip_duration >= video_duration:
            return HttpResponse("Clip duration cannot be equal to or greater than the video duration.")
        else:

            output_dir = os.path.join(settings.MEDIA_ROOT, "split_clips")
            os.makedirs(output_dir, exist_ok=True)

            start_time = 0
            clips = []
            clip_index = 0
            flag = True

            while flag:
                clip_name = f"clip_{clip_index}.mp4"
                output_clip_path = os.path.join(output_dir, clip_name)
                split_video = video_clip.subclipped(start_time, end_time)

                split_video.write_videofile(output_clip_path)

                clip_url = os.path.join(settings.MEDIA_URL, "split_clips", clip_name).replace("\\", "/")
                clips.append(clip_url)

                start_time += clip_duration
                end_time += clip_duration
                clip_index += 1

                if end_time > video_duration:
                    clip_name = f"clip_{clip_index}.mp4"
                    output_clip_path = os.path.join(output_dir, clip_name)
                    split_video = video_clip.subclipped(start_time, video_duration)
                    split_video.write_videofile(output_clip_path)

                    clip_url = os.path.join(settings.MEDIA_URL, "split_clips", clip_name).replace("\\", "/")
                    clips.append(clip_url)

                    flag = False

            video_clip.close()

        return render(request, 'video_edit/split_video_equally_page.html', {'clips': clips})

    return render(request, 'video_edit/split_video_equally_page.html')


from zipfile import ZipFile

def download_all_clips(request):
    output_dir = os.path.join(settings.MEDIA_ROOT, "split_clips")
    zip_filename = os.path.join(settings.MEDIA_ROOT, "all_clips.zip")

    with ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_dir))

    with open(zip_filename, 'rb') as f:
        response = HttpResponse(f, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="all_clips.zip"'
        return response



# **********************Extract video Section**************************

def upload_video_and_extract_audio(request):
    if request.method == 'POST' and request.FILES.get('video_file'):
        
        uploaded_file = request.FILES['video_file']

        temp_dir = tempfile.mkdtemp()
        temp_video_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_video_path, 'wb') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        try:
            clip = VideoFileClip(temp_video_path)
            audio = clip.audio
            
            audio_file_name = os.path.splitext(uploaded_file.name)[0] + ".mp3"
            output_dir = os.path.join(settings.MEDIA_ROOT, "extracted_audio")
            os.makedirs(output_dir, exist_ok=True) 
            audio_file_path = os.path.join(output_dir, audio_file_name)
            audio.write_audiofile(audio_file_path)

            clip.close()
            audio.close()

            audio_file_url = os.path.join(settings.MEDIA_URL, "extracted_audio", audio_file_name)

            return render(request, 'video_edit/extract_audio_page.html', {
                'audio_file_url': audio_file_url,
            })

        except Exception as e:
            return HttpResponse(f"Error extracting audio: {e}")

        finally:
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)

    return render(request, 'video_edit/extract_audio_page.html')





# *********************Marge Video File**************************

def upload_and_merge_videos(request):
    if request.method == 'POST' and request.FILES.getlist('video_files'):
        # Get the uploaded video files
        uploaded_files = request.FILES.getlist('video_files')

        # Create a temporary directory to save the uploaded files
        temp_dir = tempfile.mkdtemp()

        # Save the uploaded files temporarily
        temp_video_paths = []
        for uploaded_file in uploaded_files:
            temp_video_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_video_path, 'wb') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
            temp_video_paths.append(temp_video_path)

        try:
            video_clips = [VideoFileClip(path) for path in temp_video_paths]

            merged_clip = concatenate_videoclips(video_clips, method="compose")

            merged_file_name = "merged_video.mp4"
            output_dir = os.path.join(settings.MEDIA_ROOT, "merged_videos")
            os.makedirs(output_dir, exist_ok=True)
            merged_file_path = os.path.join(output_dir, merged_file_name)
            merged_clip.write_videofile(merged_file_path, codec="libx264")

            for clip in video_clips:
                clip.close()

            merged_clip.close()
            
            merged_video_url = os.path.join(settings.MEDIA_URL, "merged_videos", merged_file_name)

            return render(request, 'video_edit/merge_videos_page.html', {
                'merged_video_url': merged_video_url,
            })

        except Exception as e:
            return HttpResponse(f"Error merging videos: {e}")

        finally:
            # Clean up the temporary video files
            for path in temp_video_paths:
                if os.path.exists(path):
                    os.remove(path)

    return render(request, 'video_edit/merge_videos_page.html')
