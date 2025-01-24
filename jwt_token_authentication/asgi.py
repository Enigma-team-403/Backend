import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jwt_token_authentication.settings')

# Initialize Django ASGI application early to ensure the AppRegistry is populated
django_asgi_app = get_asgi_application()

# Import consumers after Django setup
from chat_app import consumers  # Import your consumers after Django is initialized

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/<int:chat_id>/", consumers.ChatConsumer.as_asgi()),
        ])
    ),
})