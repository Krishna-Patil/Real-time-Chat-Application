import json

from django.db.utils import IntegrityError

# from rest_framework_simplejwt.exceptions import TokenError
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .utils import extract_token_ws
from users.utils import get_user
from users.models import CustomUser
from chatapp.models import Channel


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        headers = self.scope['headers']
        token = extract_token_ws(headers)
        user = get_user(token)
        self.scope['user'] = user
        # handling if user was not able to disconnect because of some issues
        try:
            c = Channel.objects.create(user_id=self.scope['user'].id, name=self.channel_name)
            c.save()
        except IntegrityError:
            c = Channel.objects.get(user_id=self.scope['user'].id)
            c.name = self.channel_name
            c.save()
        except AttributeError:
            self.send(json.dumps({
                "error": "Not a valid token!"
            }))
            self.close()


    def disconnect(self, close_code):
        try:
            Channel.objects.get(name=self.channel_name).delete()
        except Channel.DoesNotExist:
            pass

    # Receive message from WebSocket
    def receive(self, text_data):
        json_data = json.loads(text_data)
        try:
            message = json_data["message"]
            to_user = json_data["to_user"]
        except KeyError:
            self.send(json.dumps({
                "error": "'message' and 'to_user' required!"
        }))
            self.close()

        try:
            user = CustomUser.objects.get(username=to_user)
        except CustomUser.DoesNotExist:
            self.send(json.dumps({
                "error": "User does not exist!"
            }))
            self.close()
        try:
            channel_name = Channel.objects.get(user_id=user.id).name
        except Channel.DoesNotExist:
            self.send(json.dumps({
                "error": "User is not available!"
            }))
            self.close()

        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.send)(channel_name, {
                "type": "chat.message",
                "from_user": self.scope['user'].username,
                "message": message
            })
        except UnboundLocalError:
            pass
    def chat_message(self, event):
        self.send(json.dumps({
            "from": event['from_user'],
            "message": event['message']
        }))


