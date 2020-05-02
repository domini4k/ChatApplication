from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_room_list(user):
        qs = Message.objects.filter(author=user).values_list('conv_name_id', flat=True).distinct()
        return list(Room.objects.all().values_list("name", flat=True).filter(id__in=qs))

    def last_message(user):
        qs = Message.objects.filter(author=user).values_list('conv_name_id', flat=True).distinct()
        last_messages_list = []
        for lobby in qs:
            last_message = Message.objects.order_by('-timestamp').values_list("content").filter(conv_name=lobby)[0]
            last_messages_list.extend(last_message)
        return last_messages_list


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conv_name = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username

    def last_10_messages(data):
        qs = Message.objects.filter(conv_name=data).order_by('-timestamp')[:10]
        return Message.objects.filter(id__in=qs).reverse()


