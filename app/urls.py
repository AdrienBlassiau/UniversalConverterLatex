from django.contrib import admin
from django.urls import include, path
from django.http import  HttpResponseNotFound
from django.http import Http404
from django.shortcuts import render
from . import views
from django.conf.urls import url

app_name = 'app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('latex_image', views.latex_converter_string_to_pdf, name='latex_converter_string_to_pdf'),
    path('latex_pdf', views.latex_converter_pdf, name='latex_converter_pdf'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
     url(r'^ajax/manage_dropdown/$', views.manage_dropdown, name='manage_dropdown'),
]