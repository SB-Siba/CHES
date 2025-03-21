import json
from django.db import models
from app_common.models import User
from django.utils import timezone

class Message(models.Model):
    MSGSTATUS = [
        ('Nothing', 'Nothing'),
        ('Start', 'Start'),
    ]
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    messages = models.JSONField(blank=True,null=True)
    is_read = models.BooleanField(default=False)
    message_status = models.CharField(max_length=20, choices=MSGSTATUS,default="Nothing")
    last_message = models.TextField(blank=True, null=True)  # Field to store the last message

    def save(self, *args, **kwargs):
    # Check if the messages field has any content and update the last_message field accordingly
        if self.messages:
            try:
                # Convert the JSON string to a list of messages
                message_list = json.loads(self.messages)

                # Ensure the list contains at least one message
                if isinstance(message_list, list) and len(message_list) > 0:
                    # Extract the last message in the list
                    self.last_message = message_list[-1].get('message', '')
            except (json.JSONDecodeError, IndexError, KeyError) as e:
                print(f"Error processing last message: {e}")
                self.last_message = None  # Set to None if there's an error
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
        