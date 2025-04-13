from django.db import models
from django.utils import timezone
import os

def video_upload_path(instance, filename):
    # Generate a unique path for the uploaded video
    return f'uploads/{timezone.now().strftime("%Y%m%d_%H%M%S")}_{filename}'

def audio_upload_path(instance, filename):
    # Generate a unique path for the converted audio
    return f'converted/{timezone.now().strftime("%Y%m%d_%H%M%S")}_{filename}'

class VideoFile(models.Model):
    video_file = models.FileField(upload_to=video_upload_path, max_length=255)
    audio_file = models.FileField(upload_to=audio_upload_path, null=True, blank=True, max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    converted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending', 
                            choices=[
                                ('pending', 'Pending'),
                                ('processing', 'Processing'),
                                ('completed', 'Completed'),
                                ('failed', 'Failed')
                            ])
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return os.path.basename(self.video_file.name)

    def delete(self, *args, **kwargs):
        # Delete the files when the model instance is deleted
        if self.video_file:
            if os.path.isfile(self.video_file.path):
                os.remove(self.video_file.path)
        if self.audio_file:
            if os.path.isfile(self.audio_file.path):
                os.remove(self.audio_file.path)
        super().delete(*args, **kwargs)
