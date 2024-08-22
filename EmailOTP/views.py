from django.core.mail import send_mail
from django.utils import timezone
from django.http import JsonResponse
from .models import OTP
import random
import string
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from EmailIntigration.views import send_template_email
import json

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'})
        print("Hiii")
        print(email)
        otp_code = generate_otp()
        expires_at = timezone.now() + timedelta(minutes=10)

        OTP.objects.update_or_create(
            email=email,
            defaults={'otp_code': otp_code, 'expires_at': expires_at}
        )
        send_template_email(
            subject="Your OTP Code",
            template_name="mail_template/otp_validation_mail.html",
            context={'otp_code': otp_code},
            recipient_list=[email]
        )
        return JsonResponse({'success': True, 'message': 'OTP sent to your email.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})


@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            otp_code = data.get('otp')

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'})
        print(email,otp_code)
        try:
            otp = OTP.objects.get(email=email, otp_code=otp_code)
            if otp.is_valid(otp_code):
                otp.delete()  # Delete OTP after successful verification
                return JsonResponse({'success': True, 'message': 'OTP verified successfully.'})
            else:
                return JsonResponse({'success': False, 'message': 'OTP has expired.'})
        except OTP.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid OTP.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})