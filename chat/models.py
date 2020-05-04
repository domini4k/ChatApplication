from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


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

    # All three below are used to fetch last information about conversations user is part of such as:
    # all rooms that user can see, last message in that conversation and the author of that message.
    def get_room_list(user):
        qs = Message.objects.filter(author=user).values_list('conv_name_id', flat=True).distinct()
        room_list = []
        for lobby_id in qs:
            room_list.append(Room.objects.all().values_list("name", flat=True).filter(id=lobby_id)[0])
        return room_list

    def last_message(user):
        qs = Message.objects.filter(author=user).values_list('conv_name_id', flat=True).distinct()
        last_messages_list = []
        for lobby in qs:
            last_message = Message.objects.order_by('-timestamp').values_list("content").filter(conv_name=lobby)[0][0]
            if len(last_message) > 20:
                last_message = last_message[:28]+'...'
            last_messages_list.append(last_message)
        return last_messages_list

    def last_author(user):
        qs = Message.objects.filter(author=user).values_list('conv_name_id', flat=True).distinct()
        last_authors_list = []
        for lobby in qs:
            last_author_id = str(Message.objects.order_by('-timestamp').values_list("author").filter(conv_name=lobby)[0])[1:-2]
            last_author = (User.objects.filter(id=last_author_id).values_list('username'))[0]
            last_authors_list.extend(last_author)
        return last_authors_list
