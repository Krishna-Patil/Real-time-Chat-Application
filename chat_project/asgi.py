import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from chatapp.routing import websocket_urlpatterns as chat_urls
from api.routing import websocket_urlpatterns as api_urls

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

chat_urls.extend(api_urls)

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(
                chat_urls
            )),
        )

    }
)