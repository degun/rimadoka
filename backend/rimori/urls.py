from django.urls import path

from . import views

urlpatterns = [
    path('browse/', views.browse, name='browse'),
    path('rhymes/', views.rhymes, name='rhymes'),
]