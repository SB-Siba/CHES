from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect, render
from app_common import models as common_models
from .serializers import PendingUserSerializer,AdminSiteGardeningProfileSerializer, VendorDetailsSerializer, ServiceProviderDetailsSerializer,QuizAnswersSerializer
from drf_yasg.utils import swagger_auto_schema
from . import swagger_doc as swagger_documentation
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .utils import IsSuperuser


def is_superuser(user):
    return user.is_superuser


@method_decorator(csrf_exempt, name='dispatch')
class PendingUserAPIView(APIView):
    permission_classes = [IsSuperuser]

    def get(self, request):
        not_approvedlist = common_models.User.objects.filter(is_approved=False).order_by('-id')
        serializer = PendingUserSerializer(not_approvedlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class ApproveUserAPIView(APIView):
    permission_classes = [IsSuperuser]

    def post(self, request, pk):
        user = get_object_or_404(common_models.User, id=pk)
        coins = request.query_params.get('coins', None)
        user.is_approved = True
        if coins:
            user.wallet = 500 + int(coins)
        else:
            user.wallet = 500 + user.quiz_score
        user.coins = 100
        user.save()
        return Response({'message': 'The account has been approved successfully!'}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class RejectUserAPIView(APIView):
    permission_classes = [IsSuperuser]

    def delete(self, request, pk):
        user = get_object_or_404(common_models.User, id=pk)
        user.delete()
        return Response({'message': 'The account has been rejected and deleted.'}, status=status.HTTP_200_OK)


class UserGardeningDetailsAPIView(APIView):
    permission_classes = [IsSuperuser]

    @swagger_auto_schema(
        manual_parameters=swagger_documentation.gardening_details_get,
        responses={200: AdminSiteGardeningProfileSerializer, 404: 'User not found'}
    )
    def get(self, request, pk):
        user = get_object_or_404(common_models.User, id=pk)
        gardening_data = get_object_or_404(common_models.GardeningProfile, user=user)
        serializer = AdminSiteGardeningProfileSerializer(gardening_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VendorDetailsAPIView(APIView):
    permission_classes = [IsSuperuser]

    @swagger_auto_schema(
        manual_parameters=swagger_documentation.vendor_details_get,
        responses={200: VendorDetailsSerializer, 404: 'User not found'}
    )
    def get(self, request, pk):
        user = get_object_or_404(common_models.User, id=pk)
        vendor_data = get_object_or_404(common_models.VendorDetails, vendor=user)
        serializer = VendorDetailsSerializer(vendor_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceProviderDetailsAPIView(APIView):
    permission_classes = [IsSuperuser]

    @swagger_auto_schema(
        manual_parameters=swagger_documentation.service_provider_details_get,
        responses={200: ServiceProviderDetailsSerializer, 404: 'User not found'}
    )
    def get(self, request, pk):
        user = get_object_or_404(common_models.User, id=pk)
        service_provider_data = get_object_or_404(common_models.ServiceProviderDetails, provider=user)
        serializer = ServiceProviderDetailsSerializer(service_provider_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizAnswersAPIView(APIView):
    permission_classes = [IsSuperuser]

    @swagger_auto_schema(
        manual_parameters=swagger_documentation.quiz_answers_get,
        responses={200: QuizAnswersSerializer, 404: 'User not found'}
    )
    def get(self, request, user_id):
        user = get_object_or_404(common_models.User, id=user_id)
        quiz_data = get_object_or_404(common_models.GaredenQuizModel, user=user)
        serializer = QuizAnswersSerializer(quiz_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=swagger_documentation.quiz_answers_post,
        responses={200: 'Quiz points updated successfully', 404: 'User not found'}
    )
    def post(self, request, user_id):
        user = get_object_or_404(common_models.User, id=user_id)
        quiz_points = request.query_params.get('quiz_points')
        user.quiz_score += int(quiz_points)
        user.save()
        return Response({'message': 'Quiz points updated successfully'}, status=status.HTTP_200_OK)
