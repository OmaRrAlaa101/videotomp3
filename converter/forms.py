from django import forms
from .models import VideoFile

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoFile
        fields = ['video_file']
        widgets = {
            'video_file': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'video/mp4',
                'id': 'video-upload'
            })
        }

    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        if video_file:
            if not video_file.name.endswith('.mp4'):
                raise forms.ValidationError('Please upload an MP4 file.')
            if video_file.size > 100 * 1024 * 1024:  # 100MB limit
                raise forms.ValidationError('File size must be less than 100MB.')
        return video_file 