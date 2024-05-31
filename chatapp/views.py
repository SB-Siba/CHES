from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from app_common.models import User,SellProduce,ProductFromVendor
from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models import Q
from django.db.models import Max
from django.db.models.functions import Coalesce
from itertools import zip_longest
from operator import itemgetter
from django.utils import timezone


def fetch_user_details(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        user_details = {
            'name': user.full_name,  # You can customize this to return any user details you need
            'email': user.email,    # For example, username, email, profile image URL, etc.
            'user_image': user.user_image.url if user.user_image else None
        }
        return JsonResponse(user_details)
    
@login_required
def chat(request):
    # Retrieve all users except the current user
    messages = Message.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
    sorted_messages = []

    # Process each message
    for msg in messages:
        try:
            # Convert JSON string to a list of dictionaries
            message_data = json.loads(msg.messages)
            
            # Extract the latest message
            last_message = message_data[-1]
            
            # Extract timestamp from the message dictionary
            timestamp = last_message.get('timestamp')
                
            # Append message and timestamp tuple to the list
            if timestamp:
                sorted_messages.append((timestamp, msg))
        except (AttributeError, json.JSONDecodeError, IndexError):
            # Handle errors if 'messages' field is not a JSON string,
            # does not contain 'timestamp' key, or if the list is empty
            pass

    # Sort messages based on timestamp and extract the message objects
    sorted_messages = [msg for _, msg in sorted(sorted_messages, key=itemgetter(0), reverse=True)]

    user_last_message = []
    try:
        for message in sorted_messages:
            try:
                # Convert JSON string to a list of dictionaries
                message_data = json.loads(message.messages)
            
                # Extract the last message from the list
                last_message = message_data[-1]
                
                # Extract hour and minute from timestamp
                timestamp = timezone.localtime(timezone.datetime.strptime(last_message['timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z"))
                formatted_time = timestamp.strftime("%I:%M %p") 

                # Append the last message and its formatted time to the list
                user_last_message.append((last_message['message'], formatted_time))
            except (json.JSONDecodeError, IndexError, KeyError):
                # Handle errors if the JSON string cannot be decoded, 
                # the list is empty, or if 'timestamp' key is not found
                pass
    except:
        pass

    zipped_messages = zip_longest(sorted_messages, user_last_message)

    context = {
        'zipped_messages': zipped_messages,
        }
    if request.user.is_gardener:
        return render(request, 'chat/messages.html', context)
    else:
        return render(request, 'chat/vendor_message_box.html', context)


def start_messages(request, r_id,product_id):
    # Retrieve the receiver object if it exists
    receiver = get_object_or_404(User, pk=r_id)
    try:
        product_obj = get_object_or_404(SellProduce,pk=product_id)
        initial_message = f"Hi {receiver.full_name}, I am interested in purchasing {product_obj.product_name}."
    except:
        product_obj = get_object_or_404(ProductFromVendor,pk=product_id)
        initial_message = f"Hi {receiver.full_name}, I am interested in purchasing {product_obj.name}."
    sender = request.user
    
    # Check if a message with the same sender and receiver already exists
    existing_message = Message.objects.filter(sender=sender, receiver=receiver).exists()
    
    # If a message already exists, redirect back with a message
    if existing_message:
        return redirect('chat:all_messages')
    
    # initial_message = f"Hi {receiver.full_name}, I am interested in purchasing {product_obj.product_name}."
    message_data = {
        'sender': sender.id,
        'message': initial_message,
        'timestamp': timezone.now().isoformat(),
    }
    messages_json = json.dumps([message_data])
    # If the receiver does not exist, create a new message object
    msg_obj = Message(sender=sender, receiver=receiver, message_status="Start", messages=messages_json)
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
        # Retrieve existing messages or initialize an empty list
        existing_messages = Message.objects.filter(Q(sender=request.user,receiver = receiver) | Q(sender=receiver,receiver = request.user)).values_list('messages', flat=True)
        if existing_messages and existing_messages[0] is not None:
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
            message.is_read = False
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
        

        messages_objs = Message.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
        try:
            for message in messages_objs:
                messages_dict = json.loads(message.messages)
            
                last_message_index = len(messages_dict) - 1
                last_message = messages_dict[last_message_index]
                 
                if int(last_message['sender']) == request.user.id:
                    message.is_read = True
                    message.save()
                else:
                    message.is_read = False
                    message.save()
        except:
            pass

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