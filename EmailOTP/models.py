from django.db import models
from django.utils import timezone

class OTP(models.Model):
    email = models.EmailField(unique=True)
    otp_code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()

    def is_valid(self, input_code):
        if timezone.now() >= self.expires_at:
            return False
        
        return self.otp_code == input_code

    def __str__(self):
        return f"OTP for {self.email} - Code: {self.otp_code}"
