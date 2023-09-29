from django.contrib.auth import get_user_model

from channels.testing import WebsocketCommunicator
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from .consumers import ChatConsumer


class MyTests(APITestCase):
    def setUp(self) -> None:
        """
        setting up test environment data
        """
        User = get_user_model()
        self.test_user = User.objects.create_user(
            username="test", email="test@email.com", password="testpass123"
        )
        data = {
            "username": self.test_user.username,
            "password": self.test_user.password,
        }

        if self.client.login(**data):
            self.test_user.is_online = True
        refresh = RefreshToken.for_user(self.test_user)
        response = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        token = f"Bearer {response['access']}".encode("utf-8")
        self.headers = [
            (b"sec-websocket-version", b"13"),
            (b"sec-websocket-key", b"qLH7glVXfRjac9ec2ckt3A=="),
            (b"connection", b"Upgrade"),
            (b"upgrade", b"websocket"),
            (b"origin", b"http://127.0.0.1:8000"),
            (b"authorization", token),
            (
                b"sec-websocket-extensions",
                b"permessage-deflate; client_max_window_bits",
            ),
            (b"host", b"127.0.0.1:8000"),
        ]

    async def test_chat_send_api(self):
        """
        tests ChatConsumer api view
        """
        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(), "api/chat/send/", headers=self.headers
        )
        connected, subprotocol = await communicator.connect()
        assert connected
        # Test sending text
        await communicator.send_json_to({"to_user": "test", "message": "Hello, World!"})
        response = await communicator.receive_json_from()
        assert response == {"from": "test", "message": "Hello, World!"}
        # Close
        await communicator.disconnect()
