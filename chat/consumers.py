from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Room

User = get_user_model()


# All functions below represent how the app acts with data received and how it sends
# data further. After opening the page JavaScript sends request to fetch last 10 messages.
# All messages have certain parameters such as author, content, name of the conversation and
# timestamp which is created automatically.
# Dictionaries and json format are very useful in this particular part of the app, it is very
# convenient to use them to send the data.
# For more information how to use Django Channels check documentation and tutorial:
# https://channels.readthedocs.io/en/latest/tutorial/part_1.html
class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        conv_name = Room.objects.get_or_create(name=data['conv_name'])[0]
        messages = Message.last_10_messages(conv_name)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        room = Room.objects.get(name=data['conv_name'])
        message = Message.objects.create(
            author=author_user,
            content=data['message'],
            conv_name=room)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp),
            'conv_name': str(message.conv_name)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))