from django.contrib import admin
from django.urls import path
from university_lectures import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('sessions/', views.AvailableSessions.as_view()),
    path('sessions/<str:pk>/', views.SessionDetail.as_view()),
    path('mySessions/', views.DeanSessions.as_view()),
    path('students/', views.Students.as_view()),
    path('students/<str:pk>/', views.StudentDetail.as_view()),
    path('deans/', views.DeanList.as_view()),
    path('deans/<str:pk>/', views.DeanDetail.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)
