from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token 
from . import swagger_doccumentation
from .models import User, GardeningProfile, GaredenQuizModel, VendorDetails, ServiceProviderDetails
from .serializer import (
    RegisterSerializer,
    LoginSerializer,
    GardeningProfileSerializer,
    GardeningQuizSerializer,
    GardeningQuizDetailSerializer,
    GardeningQuizQuestionSerializer,
    VendorDetailsSerializer,
    ServiceProviderDetailsSerializer,
)
from django.contrib.auth import authenticate, login, logout

# views_api.py
class RegisterAPIView(APIView):
    @swagger_auto_schema(
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
    def get(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class GardeningDetailsAPIView(APIView):
    @swagger_auto_schema(
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
    @swagger_auto_schema(
        manual_parameters=swagger_doccumentation.vendor_details_post,
        responses={201: 'Details added successfully', 400: 'Validation error'}
    )
    def post(self, request, u_email):
        try:
            user = User.objects.get(email=u_email)
            serializer = VendorDetailsSerializer(data=request.data)
            if serializer.is_valid():
                vendor_details = serializer.save(user=user)
                return Response({'message': 'Details added successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class ServiceProviderDetailsAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=swagger_doccumentation.service_provider_details_post,
        responses={201: 'Details added successfully', 400: 'Validation error'}
    )
    def post(self, request, u_email):
        try:
            user = User.objects.get(email=u_email)
            serializer = ServiceProviderDetailsSerializer(data=request.data)
            if serializer.is_valid():
                service_provider_details = serializer.save(user=user)
                return Response({'message': 'Details added successfully'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

