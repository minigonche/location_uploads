from django.urls import path

from . import views

app_name = 'location_uploads'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_info', views.upload_info, name='upload_info')
]