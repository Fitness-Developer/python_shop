import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

# Список плохих слов
BAD_WORDS = {'сука', 'блять', 'пизда', 'шлюха'}  # Замените на реальные слова
MAX_MESSAGE_LENGTH = 20  # Максимальная длина сообщения


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        if user.is_authenticated:
            # Проверка на плохие слова и длину сообщения
            if self.is_message_valid(message):
                chat_message = await self.save_message(user, message)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': chat_message.message,
                        'username': user.username
                    }
                )
            else:
                await self.send(text_data=json.dumps({
                    'error': 'Ваше сообщение содержит недопустимые слова или слишком длинное.'
                }))

    def is_message_valid(self, message):
        # Проверяем длину сообщения и наличие плохих слов
        return len(message) <= MAX_MESSAGE_LENGTH and not any(bad_word in message for bad_word in BAD_WORDS)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    @database_sync_to_async
    def save_message(self, user, message):
        from .models import ChatMessage  # Импортируем здесь
        return ChatMessage.objects.create(room_name=self.room_name, user=user, message=message)




