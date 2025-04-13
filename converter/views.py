from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import VideoFile
from .forms import VideoUploadForm
import os
from django.utils import timezone
import logging
import subprocess

logger = logging.getLogger(__name__)

FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"

def home(request):
    form = VideoUploadForm()
    return render(request, 'converter/home.html', {'form': form})

@csrf_exempt
def upload_video(request):
    if request.method == 'POST':
        logger.info(f"Received POST request with FILES: {request.FILES}")
        logger.info(f"Received POST request with POST data: {request.POST}")
        
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info("Form is valid, proceeding with save")
            video_file = form.save(commit=False)
            video_file.status = 'processing'
            video_file.save()
            
            try:
                # Convert video to audio
                video_path = video_file.video_file.path
                logger.info(f"Video path: {video_path}")
                
                audio_path = os.path.join(
                    settings.MEDIA_ROOT,
                    'converted',
                    f"{os.path.splitext(os.path.basename(video_path))[0]}.mp3"
                )
                logger.info(f"Audio path: {audio_path}")
                
                # Ensure the output directory exists
                os.makedirs(os.path.dirname(audio_path), exist_ok=True)
                
                # Use subprocess directly with ffmpeg command
                try:
                    logger.info(f"Using FFmpeg at: {FFMPEG_PATH}")
                    result = subprocess.run([
                        FFMPEG_PATH,
                        '-i', video_path,
                        '-vn',  # No video
                        '-acodec', 'libmp3lame',
                        '-y',  # Overwrite output file
                        audio_path
                    ], check=True, capture_output=True, text=True)
                    
                    logger.info(f"FFmpeg output: {result.stdout}")
                    if result.stderr:
                        logger.warning(f"FFmpeg warnings: {result.stderr}")
                    
                    # Update the model with the converted file
                    video_file.audio_file = os.path.relpath(audio_path, settings.MEDIA_ROOT)
                    video_file.status = 'completed'
                    video_file.converted_at = timezone.now()
                    video_file.save()
                    
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Video converted successfully',
                        'download_url': video_file.audio_file.url
                    })
                    
                except subprocess.CalledProcessError as e:
                    logger.error(f"FFmpeg error: {e.stderr}")
                    video_file.status = 'failed'
                    video_file.error_message = f"FFmpeg error: {e.stderr}"
                    video_file.save()
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Error converting video: FFmpeg process failed'
                    }, status=500)
                
            except Exception as e:
                logger.error(f"Error during conversion: {str(e)}", exc_info=True)
                video_file.status = 'failed'
                video_file.error_message = str(e)
                video_file.save()
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)
        else:
            logger.error(f"Form validation errors: {form.errors}")
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid form data'
            }, status=400)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
