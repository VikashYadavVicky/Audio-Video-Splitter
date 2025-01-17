
import os
import tempfile
from moviepy import AudioFileClip,concatenate_audioclips
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse


def audio_tools(request):
    return render(request, 'audio_edit/audio_tools/audio_tools.html')


# *********************Split audio File**************************

def upload_audio_and_split(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        uploaded_file = request.FILES['audio_file']
        
        temp_dir = tempfile.mkdtemp()
        temp_audio_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_audio_path, 'wb') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
        
        start_time = int(request.POST.get('start_time', 0)) 
        end_time = int(request.POST.get('end_time', 0)) 

        clip = AudioFileClip(temp_audio_path)
        total_duration = clip.duration

        if end_time == 0 or end_time > total_duration:
            end_time = total_duration 
        
        if start_time >= end_time:
            return HttpResponse("Invalid start and end times. Start time must be less than end time.")
        
        sliced_clip = clip.subclipped(start_time, end_time)

        sliced_file_name = "sliced_audio.mp3"
        sliced_file_path = os.path.join(settings.MEDIA_ROOT, "split_clips", sliced_file_name)
        sliced_clip.write_audiofile(sliced_file_path)
        
        clip.close()
        sliced_clip.close()

        sliced_audio_url = os.path.join(settings.MEDIA_URL, "split_clips", sliced_file_name)
        
        return render(request, 'audio_edit/split_audio_page.html', {
            'sliced_audio_url': sliced_audio_url
        })

    return render(request, 'audio_edit/split_audio_page.html')


# *********************Split audio Equally File**************************


def split_audio_equally(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        uploaded_file = request.FILES['audio_file']

        if not uploaded_file.name.endswith(('.mp3', '.wav', '.ogg')):
            return HttpResponse("Unsupported file format. Please upload a valid audio file.")

        temp_dir = tempfile.mkdtemp()
        temp_audio_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_audio_path, 'wb') as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)

        try:
            audio_clip = AudioFileClip(temp_audio_path)
            audio_duration = audio_clip.duration
        except Exception as e:
            return HttpResponse(f"Error loading audio file: {str(e)}")
        
        clip_duration = int(request.POST.get('clip_time', 0))
        end_time = clip_duration

        if clip_duration <= 0:
            return HttpResponse("Clip duration must be greater than 0.")
        elif clip_duration >= audio_duration:
            return HttpResponse("Clip duration cannot be equal to or greater than the audio duration.")
        else:
            output_dir = os.path.join(settings.MEDIA_ROOT, "split_clips")
            os.makedirs(output_dir, exist_ok=True)

            start_time = 0
            clips = []
            clip_index = 0
            flag = True

            while flag:
                clip_name = f"clip_{clip_index}.mp3"
                output_clip_path = os.path.join(output_dir, clip_name)
                split_audio = audio_clip.subclipped(start_time, end_time)

                split_audio.write_audiofile(output_clip_path)

                clip_url = os.path.join(settings.MEDIA_URL, "split_clips", clip_name).replace("\\", "/")
                clips.append(clip_url)

                start_time += clip_duration
                end_time += clip_duration
                clip_index += 1

                if end_time > audio_duration:
                    clip_name = f"clip_{clip_index}.mp3"
                    output_clip_path = os.path.join(output_dir, clip_name)
                    split_audio = audio_clip.subclipped(start_time, audio_duration)
                    split_audio.write_audiofile(output_clip_path)

                    clip_url = os.path.join(settings.MEDIA_URL, "split_clips", clip_name).replace("\\", "/")
                    clips.append(clip_url)

                    flag = False

            audio_clip.close()

        return render(request, 'audio_edit/split_audio_equally_page.html', {'clips': clips})

    return render(request, 'audio_edit/split_audio_equally_page.html')


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



# *********************Marge audio File**************************


def upload_and_merge_audio(request):
    if request.method == 'POST' and request.FILES.getlist('audio_files'):
        uploaded_files = request.FILES.getlist('audio_files')

        temp_dir = tempfile.mkdtemp()

        temp_audio_paths = []
        for uploaded_file in uploaded_files:
            temp_audio_path = os.path.join(temp_dir, uploaded_file.name)
            with open(temp_audio_path, 'wb') as temp_file:
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)
            temp_audio_paths.append(temp_audio_path)

        try:
            audio_clips = [AudioFileClip(path) for path in temp_audio_paths]

            merged_audio = concatenate_audioclips(audio_clips)

            merged_audio_file_name = "merged_audio.mp3"
            output_dir = os.path.join(settings.MEDIA_ROOT, "merged_audio")
            os.makedirs(output_dir, exist_ok=True)
            merged_audio_file_path = os.path.join(output_dir, merged_audio_file_name)
            merged_audio.write_audiofile(merged_audio_file_path)

            for clip in audio_clips:
                clip.close()

            merged_audio.close()

            merged_audio_url = os.path.join(settings.MEDIA_URL, "merged_audio", merged_audio_file_name)

            return render(request, 'audio_edit/merge_audio_page.html', {
                'merged_audio_url': merged_audio_url,
            })

        except Exception as e:
            return HttpResponse(f"Error merging audio files: {e}")

        finally:
            for path in temp_audio_paths:
                if os.path.exists(path):
                    os.remove(path)

    return render(request, 'audio_edit/merge_audio_page.html')
