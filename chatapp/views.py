from django.shortcuts import render
from django.urls import reverse
from users.models import CustomUser
from .models import Message
from django.db.models import Q
from django.http import HttpResponseRedirect


def homepage(request):
    users = CustomUser.objects.filter(is_online=True).values('username', 'id')
    return render(request, 'home.html', context={'users': users})


def chatpage(request, id):
    request.session['id'] = id
    user = CustomUser.objects.get(id=id)
    conversation_id = ''.join(sorted((user.email).replace('@', '-') + (request.user.email).replace('@', '-')))
    return HttpResponseRedirect(reverse('conversation', args=[conversation_id]))


def chat_ch(request, conversation_id):
    id = request.session['id']
    user = CustomUser.objects.get(id=id)
    criteria1 = (Q(from_user=request.user.id) & Q(to_user=id))
    criteria2 = (Q(from_user=id) & Q(to_user=request.user.id))
    messages = Message.objects.filter(criteria1 | criteria2).order_by('timestamp')
    format = "%d-%b-%Y %I:%M %p"
    messages = [f"{(msg.timestamp).strftime(format)} {msg.text} -- {msg.from_user}"
                for msg in messages
            ]
    context={'usr': user,
             'messages': messages, 
             'room_name': conversation_id
            }
    return render(request, 'chat_ch.html', context)
  