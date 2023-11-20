from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from main_app.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/chat/<int:match_id>/", ChatConsumer.as_asgi()),
    ]),
})
