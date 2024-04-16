from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from app_common.models import User
from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

@login_required
def chat(request):
    # Retrieve all users except the current user
    messages = Message.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
    context = {'messages': messages}
    return render(request, 'chat/messages.html', context)


def start_messages(request, r_id):
    # Retrieve the receiver object if it exists
    receiver = get_object_or_404(User, pk=r_id)
    
    sender = request.user
    
    # Check if a message with the same sender and receiver already exists
    existing_message = Message.objects.filter(sender=sender, receiver=receiver).exists()
    
    # If a message already exists, redirect back with a message
    if existing_message:
        return redirect('chat:all_messages')
    
    # If the receiver does not exist, create a new message object
    msg_obj = Message(sender=sender, receiver=receiver, message_status="Start")
    msg_obj.save()
    
    return redirect('chat:all_messages')

from django.utils import timezone
import json

@login_required
def send_message(request):
    if request.method == 'POST':
        sender = request.user
        receiver_id = request.POST.get('receiver_id')
        receiver = get_object_or_404(User, pk=receiver_id)
        message = request.POST.get('message')
        print(f"Message received: {message}")
        # Retrieve existing messages or initialize an empty list
        existing_messages = Message.objects.filter(Q(sender=request.user,receiver = receiver) | Q(sender=receiver,receiver = request.user)).values_list('messages', flat=True)
        if existing_messages and existing_messages[0] is not None:
            print("yess")
            messages = json.loads(existing_messages[0])
        else:
            messages = []

        # Append the new message to the list of messages
        message_data = {
            'sender': sender.id,
            'message': message,
            'timestamp': timezone.now().isoformat(),
        }
        messages.append(message_data)

        # Update the JSONField with the new messages
        messages_to_update = Message.objects.filter(
            Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)
        )

        # Update the messages
        for message in messages_to_update:
            # Update each message with the new messages value
            message.messages = json.dumps(messages)
            message.save()

        # Redirect back to the chat page or any other page you prefer
        return redirect('chat:all_messages')
    else:
        # Handle if it's not a POST request
        return HttpResponseBadRequest("Invalid request method")

def fetch_messages(request):
    if request.method == 'GET':
        # Fetch the receiver ID from the request
        receiver_id = request.GET.get('receiver_id')
        
        # Retrieve the receiver object
        receiver = get_object_or_404(User, pk=receiver_id)
        
        # Retrieve the messages sent to the receiver
        messages = Message.objects.filter(Q(sender=request.user,receiver = receiver) | Q(sender=receiver,receiver = request.user)).values_list('messages', flat=True)
        f_messages = [msg for msg in messages if msg is not None]
        print(f_messages)
        if len(f_messages) > 0:
            sender_id = request.user.id
            response_data = {
                'messages': json.loads(messages[0]),
                'senderId': sender_id
            }
            return JsonResponse(response_data, safe=False)
        else:
            sender_id = request.user.id
            response_data = {
                'messages': [],    
                'senderId': sender_id
            }
            return JsonResponse(response_data, safe=False)
    else:
        # Handle if it's not a GET request
        return HttpResponseBadRequest("Invalid request method")