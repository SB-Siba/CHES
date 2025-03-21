from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserRankSerializer
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from . import swagger_doccumentation
from drf_yasg import openapi


class TopRTGUsersAPIView(APIView):
    @swagger_auto_schema(
        tags=["Top Users Rank of RTG"],
        operation_description="Top RTG User according to points",
        manual_parameters=swagger_doccumentation.top_users_params,
        responses={
            200: openapi.Response('OTP sent successfully', examples={'application/json': {'success': True, 'message': 'OTP sent to your email.'}}),
            400: 'Invalid request',
        }
    )
    def get(self, request):
        try:
            top_users = User.objects.filter(
                is_active=True,
                is_approved=True
            ).filter(
                Q(is_rtg=True)
                
            ).order_by('-coins')

            serializer = UserRankSerializer(top_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TopVendorUsersAPIView(APIView):
    @swagger_auto_schema(
        tags=["Top Users Rank of Vendor"],
        operation_description="Top Vendor User according to points",
        manual_parameters=swagger_doccumentation.top_users_params,
        responses={
            200: openapi.Response('OTP sent successfully', examples={'application/json': {'success': True, 'message': 'OTP sent to your email.'}}),
            400: 'Invalid request',
        }
    )
    def get(self, request):
        try:
            top_users = User.objects.filter(
                is_active=True,
                is_approved=True
            ).filter(
                Q(is_vendor=True)
                
            ).order_by('-coins')

            serializer = UserRankSerializer(top_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
