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

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"
        