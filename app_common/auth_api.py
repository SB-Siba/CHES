from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from EmailIntigration.views import send_template_email 
from . import swagger_doccumentation
from .models import User, GardeningProfile, GaredenQuizModel, VendorDetails, ServiceProviderDetails
from .serializer import (
    AuthServiceProviderDetailsSerializer,
    ForgotPasswordSerializer,
    RegisterSerializer,
    LoginSerializer,
    GardeningProfileSerializer,
    GardeningQuizSerializer,
    GardeningQuizDetailSerializer,
    GardeningQuizQuestionSerializer,
    ResetPasswordSerializer,
    VendorDetailsSerializer,
)
from rest_framework.parsers import FormParser, MultiPartParser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException
from django.urls import reverse_lazy

# views_api.py
class RegisterAPIView(APIView):
    @swagger_auto_schema(
        tags=["Authentication API'S"],
        operation_description="Registration API",
        manual_parameters=swagger_doccumentation.signup_post,
        responses={201: 'Registration successful', 400: 'Validation error'}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    @swagger_auto_schema(
        tags=["Authentication API'S"],
        operation_description="Login API",
        manual_parameters=swagger_doccumentation.login_post,
        responses={
            200: openapi.Response('Login successful'),
            400: openapi.Response('Validation error'),
            401: openapi.Response('Login failed / You are not approved yet'),
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user_obj = User.objects.filter(email = email)
            print(user_obj)
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return Response({'message': 'Login successful Admin'}, status=status.HTTP_200_OK)
                
                elif user.is_approved:
                    if user.is_rtg:
                        login(request, user)
                        token, _ = Token.objects.get_or_create(user=user)
                        return Response({'message': 'Login successful, Hii Roof Top Gardener','token': token.key}, status=status.HTTP_200_OK)
                    elif user.is_vendor:
                        login(request, user)
                        token, _ = Token.objects.get_or_create(user=user)
                        return Response({'message': 'Login successful, Hii Vendor','token': token.key}, status=status.HTTP_200_OK)
                    elif user.is_serviceprovider:
                        login(request, user)
                        token, _ = Token.objects.get_or_create(user=user)
                        return Response({'message': 'Login successful, Hii Service Provider','token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': "Your account hasn't been approved yet."}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': "Login failed / You are not approved yet !!!"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    @swagger_auto_schema(
        tags=["Authentication API'S"],
        operation_description="Logout API",
        manual_parameters=swagger_doccumentation.logout_get,
        responses={200: "log out successfull.", 404: 'Error while log out.'}
    )
    def get(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class GardeningDetailsAPIView(APIView):
    @swagger_auto_schema(
        tags=["Authentication API'S"],
        operation_description="Gardening Detail API",
        manual_parameters=swagger_doccumentation.gardening_details_post,
        responses={201: 'Details added successfully', 400: 'Validation error'}
    )
    def post(self, request, u_email):
        try:
            user = User.objects.get(email=u_email)
            serializer = GardeningProfileSerializer(data=request.data)
            if serializer.is_valid():
                gardening_details = serializer.save(user=user)
                return Response({'message': 'Details added successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class GardeningQuizAPIView(APIView):
    @swagger_auto_schema(
        tags=["Authentication API'S"],
        operation_description="Gardening Quiz API",
        manual_parameters=swagger_doccumentation.gardening_quiz_post,
        responses={201: 'Quiz submitted successfully', 400: 'Validation error'}
    )
    def post(self, request, u_email):
        try:
            user = User.objects.get(email=u_email)
            serializer = GardeningQuizSerializer(data=request.data)
            if serializer.is_valid():
                data = {
                    'What is the process of cutting off dead or overgrown branches called?': serializer.validated_data['q1'],
                    'Which of the following is a perennial flower?': serializer.validated_data['q2'],
                    'What is the best time of day to water plants?': serializer.validated_data['q3'],
                    'Which type of soil holds water the best?': serializer.validated_data['q4'],
                    'What is the primary purpose of adding compost to soil?': serializer.validated_data['q5'],
                }
                quiz_obj, created = GaredenQuizModel.objects.update_or_create(
                    user=user,
                    defaults={'questionANDanswer': data}
                )
                return Response({'message': 'Quiz submitted successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        tags=["Authentication API'S"],
        operation_description="Gardening Quiz's API",
        manual_parameters=swagger_doccumentation.gardening_quiz_get,
        responses={200: GardeningQuizQuestionSerializer, 404: 'User not found'}
    )
    def get(self, request, u_email):
        try:
            user = User.objects.get(email=u_email)
            # Manually setting default questions to the serializer
            default_questions = {
                'q1': 'What is the process of cutting off dead or overgrown branches called?',
                'q2': 'Which of the following is a perennial flower?',
                'q3': 'What is the best time of day to water plants?',
                'q4': 'Which type of soil holds water the best?',
                'q5': 'What is the primary purpose of adding compost to soil?'
            }
            serializer = GardeningQuizQuestionSerializer(default_questions)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class VendorDetailsAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Authentication API'S"],
        operation_description="Vendor Data API",
        manual_parameters=swagger_doccumentation.vendor_details_post,
        responses={201: 'Details added successfully', 400: 'Validation error'}
    )
    def post(self, request, u_email):
        try:
            user = User.objects.get(email=u_email)
            serializer = VendorDetailsSerializer(data=request.data)
            if serializer.is_valid():
                vendor_details = serializer.save(vendor=user)
                return Response({'message': 'Details added successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ServiceProviderDetailsAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Authentication API'S"],
        operation_description="API to add service provider details",
        manual_parameters=swagger_doccumentation.service_provider_details_post,
        responses={201: 'Details added successfully', 400: 'Validation error', 404: 'User not found'}
    )
    def post(self, request, u_email):
        user = User.objects.get(email=u_email)
        serializer = AuthServiceProviderDetailsSerializer(data=request.data)
        if serializer.is_valid():
            service_provider_detail = serializer.save(provider=user)
            return Response(AuthServiceProviderDetailsSerializer(service_provider_detail).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Authentication API'S"],
        operation_description="Forgot password link send to registered email.",
        manual_parameters=swagger_doccumentation.forgot_password,
        responses={201: 'forgot Password link send successfully', 400: 'Validation error'}
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(
                    reverse_lazy('app_common:password_reset_confirm_api', kwargs={'uidb64': uid, 'token': token})
                )
                subject = 'Password Reset Requested'
                message = f"""
                Hi {user.full_name},

                Click the link below to reset your password:

                {reset_link}

                If you did not request a password reset, please ignore this email.

                Thanks,
                Your Website Team
                """
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                except SMTPException as e:
                    return Response({"error": "Failed to send email. Please try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"message": "If an account with that email exists, a password reset link has been sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["Authentication API'S"],
        operation_description="Password rest done",
        manual_parameters=swagger_doccumentation.reset_password,
        responses={201: 'Password Reset successfully', 400: 'Validation error'}
    )
    def post(self, request, uidb64, token):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                new_password1 = serializer.validated_data['password']
                new_password2 = serializer.validated_data['confirm_password']
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    return Response({"message": "Password Reset Successfully Done."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Passwords doesn't match."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)