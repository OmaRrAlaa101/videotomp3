# Video to MP3 Converter

A Django web application that allows users to upload MP4 video files and convert them to MP3 audio files.

## Features

- Upload MP4 video files through drag-and-drop or file selector
- Convert videos to MP3 format
- Modern, responsive UI with Tailwind CSS
- Real-time conversion status updates
- File validation and error handling
- Automatic file cleanup

## Requirements

- Python 3.8+
- Django 5.0+
- moviepy
- django-widget-tweaks
- Pillow

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd video-converter
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create the necessary media directories:
```bash
mkdir media\uploads media\converted
```

## Running the Application

1. Start the development server:
```bash
python manage.py runserver
```

2. Open your browser and navigate to `http://localhost:8000`

## Usage

1. Click the upload area or drag and drop an MP4 file
2. Wait for the conversion process to complete
3. Download the converted MP3 file

## File Size Limits

- Maximum file size: 100MB
- Supported input format: MP4 only

## Development

To make changes to the application:

1. Modify the templates in `converter/templates/converter/`
2. Update the views in `converter/views.py`
3. Modify the models in `converter/models.py`

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure a proper database (e.g., PostgreSQL)
3. Set up proper static and media file serving
4. Use a production-grade web server (e.g., Gunicorn)
5. Set up proper security measures (HTTPS, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details. "# videotomp3" 


![image](https://github.com/user-attachments/assets/7523ad30-3b83-4988-b2a0-de280730b44b)

