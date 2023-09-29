import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Message
from users.models import CustomUser


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        to_user = CustomUser.objects.get(id=text_data_json["to_user"])
        msg = Message.objects.create(
            from_user=self.scope["user"], to_user=to_user, text=message
        )
        msg.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        format = "%d-%b-%Y %I:%M %p"
        timestamp = datetime.date(datetime.now()).strftime(format)
        message = f"{timestamp} {message} -- {self.scope['user']}"
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
  