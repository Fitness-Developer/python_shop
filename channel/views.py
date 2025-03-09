from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
from django.shortcuts import render

@csrf_exempt
def send_message(request, room_name):
    if request.method == 'POST':
        message = request.POST.get('message')
        user = request.user  # или другой способ получить пользователя

        if user.is_authenticated:
            chat_message = ChatMessage.objects.create(room_name=room_name, user=user, message=message)
            return HttpResponse(f'<p><strong>{user.username}:</strong> {message}</p>')

    return HttpResponse('Invalid request', status=400)

def chat_room(request, room_name):
    messages = ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')  # Получите все сообщения для комнаты
    return render(request, 'chat/chat_room.html', {
        'room_name': room_name,
        'messages': messages,
    })