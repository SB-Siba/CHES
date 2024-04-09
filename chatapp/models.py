from django.db import models
from app_common.models import User
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField(null=True,blank=True)