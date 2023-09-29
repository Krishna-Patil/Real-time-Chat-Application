from django.urls import path
from .views import *

urlpatterns = [
    path('home', homepage, name='home'),
    path('chat/<int:id>/', chatpage, name='chat'),
    path('chat/<str:conversation_id>/', chat_ch, name='conversation')
]