from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from .models import Message


@login_required
def index(request):
    return render(request, 'chat/index.html')


# Listed below help to iterate through lists in template "room.html"
@login_required
def room(request, room_name):
    conv_list = zip(
        Message.get_room_list(request.user),
        Message.last_author(request.user),
        Message.last_message(request.user))
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'conv_list': conv_list,
    })


