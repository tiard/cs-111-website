from django.urls import path

from . import views

app_name = 'cs111'

urlpatterns = [
    path('', views.index, name='index'),
    path('repository/', views.repository, name='repository'),
    path('lectures/', views.LecturesView.as_view(), name='lectures'),
    path('labs/', views.LabsView.as_view(), name='labs'),
    path('resources/', views.resources, name='resources'),
]
