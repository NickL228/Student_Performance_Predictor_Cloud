from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('predict/', views.predict_student, name='predict'),
    path('history/', views.history, name='history'),
    path('api/predict/', views.predict_api, name='predict_api'),
    path('api/history/', views.history_api, name='history_api'),
    path('api/users/', views.users_api, name='users_api'),
    path('api/users/delete/<int:id>/', views.delete_user_api, name='delete_user_api'),
    path('api/register/', views.register_api, name='register_api'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/logout/', views.logout_api, name='logout_api'),
    path('api/delete/<int:id>/', views.delete_prediction, name='delete_prediction'),
]