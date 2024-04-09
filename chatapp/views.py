from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from app_common.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt




def user_info(request):
    # Retrieve user information (replace this with your actual logic)
    user = request.user
    user_info = {
        'full_name': user.full_name,
        'email': user.email,
        'user_image': user.user_image.url if user.user_image  else None,
        # Add more user information as needed
    }
    # Return user information as JSON response
    return JsonResponse(user_info)


@login_required
def inbox(request):
    user = request.user
    conversations = user.received_messages.values('sender__full_name').distinct()
    return render(request, 'chat/inbox.html', {'conversations': conversations})

@login_required
def conversation_sender(request, full_name):
    user = request.user
    sender = get_object_or_404(User, full_name=full_name)
    messages = Message.objects.filter(sender=sender, recipient=request.user) | Message.objects.filter(sender=request.user, recipient=sender)
    messages = messages.order_by('timestamp')
    sender_details = {
        'full_name': sender.full_name,
        'user_image_url': sender.user_image.url if sender.user_image else None  # Assuming user_image is an ImageField
        # Add more sender details as needed
    }
    messages_data = [{
        'sender':message.sender.email,
        'content': message.content,
        'timestamp': message.timestamp,
        # Add more message fields as needed
    } for message in messages]
    
    return JsonResponse({'messages': messages_data, 'sender': sender_details})

@login_required
def conversation_reciver(request, full_name):
    recipient = get_object_or_404(User, full_name=full_name)
    messages = Message.objects.filter(recipient=recipient, sender=request.user) | Message.objects.filter(recipient=request.user, sender=recipient)
    messages = messages.order_by('timestamp')
    recipient_details = {
        'full_name': recipient.full_name,
        'user_image_url': recipient.user_image.url if recipient.user_image else None  # Assuming user_image is an ImageField
        # Add more recipient details as needed
    }
    messages_data = [{
        'sender':message.sender.email,
        'sender_image':message.sender.user_image.url if message.sender.user_image else None,
        'content': message.content,
        'timestamp': message.timestamp,
        # Add more message fields as needed
    } for message in messages]
    
    return JsonResponse({'messages': messages_data, 'recipient': recipient_details})
    

@login_required
@csrf_exempt
def compose_message(request, full_name):
    recipient = get_object_or_404(User, full_name=full_name)
 
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect('chat:all_messages')

from datetime import datetime
import pytz
def allMessages(request):
    user = request.user
    
    # Get distinct participants in conversations
    conversation_participants = set()
    conversations = Message.objects.filter(Q(recipient=user) | Q(sender=user))
    for conversation in conversations:
        if conversation.sender == user:
            conversation_participants.add((conversation.sender.full_name, conversation.recipient.full_name))
        else:
            conversation_participants.add((conversation.recipient.full_name, conversation.sender.full_name))
            # Sort by most recent first
    print("Before sorting:")
    for participant in conversation_participants:
        print(participant)

    # Sort conversation participants based on the timestamp of their last message in descending order
    sorted_conversation_participants = sorted(conversation_participants, key=lambda x: x[1], reverse=True)

    # Print the sorted list
    print("\nAfter sorting:")
    for participant in sorted_conversation_participants:
        print(participant)

    # Fetch the latest message for each conversation
    messages = []
    for sender_name, recipient_name in sorted_conversation_participants:
        
        try:
            latest_message = Message.objects.filter(
                (Q(sender__full_name=sender_name) & Q(recipient__full_name=recipient_name)) |
                (Q(sender__full_name=recipient_name) & Q(recipient__full_name=sender_name))
            ).latest('timestamp')
     
            time = str(latest_message.timestamp)
            latest_message_timestamp = datetime.fromisoformat(time)
            local_timezone = pytz.timezone('Asia/Kolkata')  # Replace with your local timezone
            latest_message_timestamp_local = latest_message_timestamp.astimezone(local_timezone)
            hour_minute = latest_message_timestamp_local.strftime('%I:%M %p')
            messages.append((hour_minute, latest_message))
        except Message.DoesNotExist:
            pass
    
    form = MessageForm()
        
    return render(request, "chat/messages.html", {'all_messages': messages, 'form': form})