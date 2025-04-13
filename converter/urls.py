from django.urls import path
from . import views

app_name = 'converter'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_video, name='upload_video'),
] 