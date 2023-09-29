from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('online-users/', OnlineUsersAPIView.as_view(), name='online_users'),
    path('chat/start/', StartChatAPIView.as_view(), name='start-chat'),
    path('suggested-friends/<int:user_id>/', SuggestFriendsAPIView.as_view(), name='suggest_friends'),
    
]