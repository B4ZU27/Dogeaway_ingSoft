"""import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Match, Chat

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.match_group_name = f"chat_{self.match_id}"

        # Unirse al grupo de la conversación
        await self.channel_layer.group_add(
            self.match_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de la conversación
        await self.channel_layer.group_discard(
            self.match_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Guardar el mensaje en la base de datos
        match = Match.objects.get(id=self.match_id)
        Chat.objects.create(
            match=match,
            remitente=self.scope['user'],
            mensaje=message
        )

        # Enviar mensaje al grupo de la conversación
        await self.channel_layer.group_send(
            self.match_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'username': self.scope['user'].username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Match, Chat
from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.chat_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'chat_id': self.chat_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        chat_id = event['chat_id']

        await self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'chat_id': chat_id
        }))

