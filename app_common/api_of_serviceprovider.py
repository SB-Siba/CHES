import datetime
import os
from django.shortcuts import get_object_or_404
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view,permission_classes
from chatapp.models import Message
from rest_framework.parsers import FormParser, MultiPartParser
from . import swagger_doccumentation
from django.contrib.auth.hashers import make_password
from .models import Booking, Order, ProduceBuy, ProductFromVendor, Service, ServiceProviderDetails, User, GardeningProfile,UserActivity,SellProduce
from .serializer import (
    BlogSerializer,
    BookingSerializer,
    ServiceProviderSerializer,
    ServiceSerializer,
    ServiceProviderProfileUpdateSerializer
)
from Blogs.models import Blogs
from user_dashboard.serializers import DirectBuySerializer,OrderSerializer
from django.contrib.auth import authenticate, login, logout
import json
from django.db.models import Q
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.utils import timezone

class ServiceProviderProfileAPI(APIView):
    @swagger_auto_schema(
        tags=["ServiceProvider API"],
        operation_description="Retrieve Service Provider Profile",
        manual_parameters=swagger_doccumentation.service_provider_profile_get,
        responses={200: ServiceProviderSerializer(many=False)}
    )
    def get(self, request):
        user = request.user
        service_provider_obj = get_object_or_404(ServiceProviderDetails, provider=user)
        serializer = ServiceProviderSerializer(service_provider_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ServiceProviderUpdateProfileAPI(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["ServiceProvider API"],
        operation_description="Update Service Provider Profile",
        request_body=ServiceProviderProfileUpdateSerializer,
        manual_parameters=swagger_doccumentation.service_provider_update_profile_post,
        responses={200: "Profile updated successfully", 400: "Invalid data provided"},
    )
    def post(self, request):
        service_provider_details = get_object_or_404(ServiceProviderDetails, provider=request.user)
        serializer = ServiceProviderProfileUpdateSerializer(instance=service_provider_details, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update user object if needed
            user_obj = request.user
            if 'image' in request.FILES:
                user_obj.user_image = request.FILES['image']
            user_obj.save()

            return Response("Profile updated successfully", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServiceListAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProvider API"],
        operation_description="All Service Lists",
        manual_parameters=swagger_doccumentation.service_list_get,
        responses={200: "Fetched successfully", 400: "Error While Fetching"},
    )

    def get(self, request):
        services = Service.objects.filter(provider=request.user)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    
    parser_classes = [FormParser, MultiPartParser]
    
    @swagger_auto_schema(
        tags=["ServiceProvider API"],
        operation_description="Add Service",
        manual_parameters=swagger_doccumentation.service_list_post,
        responses={200: "Added successfully", 400: "Error While Adding."},
    )

    def post(self, request):
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(provider=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServiceUpdateAPIView(APIView):
    def get_object(self, service_id):
        try:
            return Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            raise Http404
    @swagger_auto_schema(
        tags=["ServiceProvider API"],
        operation_description="Detail Service",
        manual_parameters=swagger_doccumentation.service_update_get,
        responses={200: "Service fetched successfully", 400: "Error while fetching."},
    )
    def get(self, request, service_id, format=None):
        service = self.get_object(service_id)
        serializer = ServiceSerializer(service)
        return Response(serializer.data)
    
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["ServiceProvider API"],
        operation_description="Update Service",
        manual_parameters=swagger_doccumentation.service_update_post,
        responses={200: "Service updated successfully", 400: "Invalid data provided"},
    )
    def put(self, request, service_id, format=None):
        service = self.get_object(service_id)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ServiceDeleteAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProvider API"],
        operation_description="Delete Service",
        manual_parameters=swagger_doccumentation.service_delete_params,
        responses={200: "Service deleted successfully", 400: "Invalid data provided"},
    )
    def delete(self, request, service_id, format=None):
        try:
            service = Service.objects.get(id=service_id)
            if service.provider != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Service.DoesNotExist:
            raise Http404



class MyServiceBookingsAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProvider API"],
        operation_description="All Service Bookings",
        manual_parameters=swagger_doccumentation.my_service_bookings_params,
        responses={200: "Fetched successfully", 400: "Error While Fetching"},
    )

    def get(self, request):
        bookings = Booking.objects.filter(service__provider=self.request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    

class BookingActionAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProvider API"],
        operation_description="Response to booking.",
        manual_parameters=swagger_doccumentation.booking_action_params,
        responses={200: "Action taken successfully", 400: "Invalid data provided"},
    )
    def post(self, request, booking_id, action, format=None):
        booking = get_object_or_404(Booking, id=booking_id)
        if request.user != booking.service.provider:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if action == 'confirm':
            booking.status = 'confirmed'
        elif action == 'decline':
            booking.status = 'declined'
        elif action == 'complete':
            booking.status = 'completed'
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        booking.save()
        return Response(status=status.HTTP_200_OK)
    
# ################### BLOGS

class SpBlogListAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProviderBlog"],
        operation_description="Retrieve a list of blogs for the current user",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: BlogSerializer(many=True)},
    )
    def get(self, request):
        blogs = Blogs.objects.filter(user=request.user).order_by('-id')
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

class SpBlogAddAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProviderBlog"],
        operation_description="Add a new blog",
        request_body=BlogSerializer,
        responses={201: BlogSerializer},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
    )
    def post(self, request):
        serializer = BlogSerializer(data=request.data, files=request.FILES)
        if serializer.is_valid():
            blog = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpBlogUpdateAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProviderBlog"],
        operation_description="Update an existing blog",
        request_body=BlogSerializer,
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'blog_id',
                openapi.IN_PATH,
                description="ID of the blog to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={200: BlogSerializer},
    )
    def post(self, request, blog_id):
        blog = get_object_or_404(Blogs, id=blog_id)
        serializer = BlogSerializer(blog, data=request.data, files=request.FILES, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpBlogDeleteAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProviderBlog"],
        operation_description="Delete a blog",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'blog_id',
                openapi.IN_PATH,
                description="ID of the blog to delete",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={204: 'No Content'},
    )
    def get(self, request, blog_id):
        blog = get_object_or_404(Blogs, id=blog_id)
        if blog.image:
            os.remove(blog.image.path)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SpBlogViewAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProviderBlog"],
        operation_description="Retrieve a list of approved blogs",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: BlogSerializer(many=True)},
    )
    def get(self, request):
        blogs = Blogs.objects.filter(is_accepted="approved")
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

class SpBlogDetailsAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProviderBlog"],
        operation_description="Retrieve details of a specific blog",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'slug',
                openapi.IN_PATH,
                description="Slug of the blog",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: BlogSerializer},
    )
    def get(self, request, slug):
        blog = get_object_or_404(Blogs, slug=slug)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

class SpBlogSearchAPIView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProviderBlog"],
        operation_description="Search for blogs",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'query': openapi.Schema(type=openapi.TYPE_STRING, description="Search query"),
                'filter_by': openapi.Schema(type=openapi.TYPE_STRING, description="Filter by field")
            }
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: BlogSerializer(many=True)},
    )
    def post(self, request):
        query = request.data.get('query', '')
        filter_by = request.data.get('filter_by', 'all')
        if filter_by == "id":
            blogs = Blogs.objects.filter(id=query, user=request.user)
        elif filter_by == "name":
            blogs = Blogs.objects.filter(title__icontains=query, user=request.user)
        elif filter_by == "all":
            blogs = Blogs.objects.filter(
                Q(id__icontains=query) | Q(title__icontains=query), user=request.user
            )
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)