from django.urls import path, include
from . import views

urlpatterns = [
    path('user/register/', views.RegisterApi_v3.as_view()),
]
