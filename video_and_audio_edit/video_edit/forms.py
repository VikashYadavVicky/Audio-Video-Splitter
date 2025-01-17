from django import forms
from .models import SplitVideoUpload,SplitEquallyVideoUpload,ExtractAudio,MergeVideo

class SplitVideoUploadForm(forms.ModelForm):
    class Meta:
        model = SplitVideoUpload
        fields = ['title', 'split_video_file',]
        
class SplitEquallyVideoUploadForm(forms.ModelForm):
    class Meta:
        model = SplitEquallyVideoUpload
        fields = ['title', 'split_equally_video_file',]
        
class ExtractAudioForm(forms.ModelForm):
    class Meta:
        model = ExtractAudio
        fields = ['title', 'audio_file',]
 

# multiple file input forms

# Custom widget to allow multiple file uploads
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# Custom field to handle multiple files
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        # If multiple files are selected, clean each file
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

# Define the form using the custom file field
class FileFieldForm(forms.Form):
    file_field = MultipleFileField()
