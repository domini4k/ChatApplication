from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.utils.safestring import mark_safe
import json
from .models import Room, Message


@login_required
def index(request):
    return render(request, 'chat/index.html')


@login_required
def room(request, room_name):
    conv_list = zip(
        Room.get_room_list(request.user),
        Room.last_message(request.user))
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'conv_list': conv_list,
    })


