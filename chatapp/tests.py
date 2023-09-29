from channels.testing import WebsocketCommunicator
from .consumers import ChatConsumer

async def test_chat_consumer():
    communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "ws/chat/<str:conversation_id>/" )
    connected, subprotocol = await communicator.connect()
    assert connected
    # Test sending text
    await communicator.send_to(text_data="hello")
    response = await communicator.receive_from()
    assert response == "hello"
    # Close
    await communicator.disconnect()