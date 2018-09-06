from django.urls import path

from . import views

app_name = 'location_uploads'

urlpatterns = [
    path('', views.index, name='index'),
    path('survey', views.survey, name='survey'),
    path('jsons', views.jsons, name='jsons'),
    path('terms', views.terms, name='terms'),
    path('upload_survey', views.upload_survey, name='upload_survey'),
    path('upload_json', views.upload_json, name='upload_json')
]