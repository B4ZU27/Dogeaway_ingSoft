import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.match_group_name = f"chat_{self.match_id}"

        # Unirse al grupo de chat
        await self.channel_layer.group_add(
            self.match_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de chat
        await self.channel_layer.group_discard(
            self.match_group_name,
            self.channel_name
        )

    # Recibir mensaje del WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Guardar mensaje en la base de datos
        Chat.objects.create(
            match_id=self.match_id,
            remitente=self.scope['user'],
            mensaje=message
        )

        # Enviar mensaje al grupo de chat
        await self.channel_layer.group_send(
            self.match_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'remitente': self.scope['user'].username,
            }
        )

    # Recibir mensaje del grupo de chat
    async def chat_message(self, event):
        message = event['message']
        remitente = event['remitente']

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'remitente': remitente,
        }))
