# # mysite/asgi.py
# import os

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.core.asgi import get_asgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# # Initialize Django ASGI application early to ensure the AppRegistry
# # is populated before importing code that may import ORM models.
# django_asgi_app = get_asgi_application()

# from chat.routing import websocket_urlpatterns

# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
#         ),
#     }
# )

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import OriginValidator, AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websock.settings')

django_asgi_app = get_asgi_application()

from echo import routing as echo_routing
from chat import routing as chat_routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            AuthMiddlewareStack(
                URLRouter(
                    echo_routing.websocket_urlpatterns +
                    chat_routing.websocket_urlpatterns
                )
            )
        )
    )
})