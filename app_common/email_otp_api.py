from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from EmailOTP.models import OTP
import random
import string
from datetime import timedelta
from EmailIntigration.views import send_template_email
from . import swagger_doccumentation
from rest_framework.parsers import FormParser, MultiPartParser


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

class SendOTPAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["Otp Api"],
        operation_description="Send OTP to the provided email",
        manual_parameters=swagger_doccumentation.send_otp_params,
        responses={
            200: openapi.Response('OTP sent successfully', examples={'application/json': {'success': True, 'message': 'OTP sent to your email.'}}),
            400: 'Invalid request',
        }
    )
    def post(self, request):
        email = request.POST.get('email')  # Using request.POST since we expect form data
        if not email:
            return Response({'success': False, 'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

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

        return Response({'success': True, 'message': 'OTP sent to your email.'}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["Otp Api"],
        operation_description="Verify the OTP for the given email",
        manual_parameters=swagger_doccumentation.verify_otp_params,
        responses={
            200: openapi.Response('OTP verified successfully', examples={'application/json': {'success': True, 'message': 'OTP verified successfully.'}}),
            400: 'Invalid request',
            404: 'Invalid OTP or OTP expired',
        }
    )
    def post(self, request):
        email = request.POST.get('email')  # Using request.POST since we expect form data
        otp_code = request.POST.get('otp')  # Using request.POST for form data

        if not email or not otp_code:
            return Response({'success': False, 'message': 'Email and OTP are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp = OTP.objects.get(email=email, otp_code=otp_code)

            if otp.is_valid(otp_code):
                otp.delete()  # Delete OTP after successful verification
                return Response({'success': True, 'message': 'OTP verified successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'message': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({'success': False, 'message': 'Invalid OTP.'}, status=status.HTTP_404_NOT_FOUND)