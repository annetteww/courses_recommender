from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('parse/', views.parse_courses, name='parse_courses'),
    path('recommend/', views.recommend_courses, name='recommend'),
]
