from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("api/chat/send/", consumers.ChatConsumer.as_asgi())
]