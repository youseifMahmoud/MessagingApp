# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('communicating_with_others/', views.communicating_with_others, name='communicating_with_others'),
    path('chat/<int:user_id>/', views.chat_with_user, name='chat_with_user'),
]
