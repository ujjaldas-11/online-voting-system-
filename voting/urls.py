from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('vote/', views.vote, name='vote'),
    path('results/', views.results, name='results'),
    path('api/results/', views.results_api, name='results_api'),
]
