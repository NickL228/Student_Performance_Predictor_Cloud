from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_student, name='predict'),
    path('history/', views.history, name='history'),
]