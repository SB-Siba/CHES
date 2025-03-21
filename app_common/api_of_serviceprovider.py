import os
from django.shortcuts import get_object_or_404
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from . import swagger_doccumentation
from django.contrib.auth.hashers import make_password
from .models import Booking,Service, ServiceProviderDetails
from .serializer import (
    BlogSerializer,
    BookingSerializer,
    ServiceProviderSerializer,
    ServiceSerializer,
    ServiceProviderProfileUpdateSerializer
)
from Blogs.models import Blogs
from django.http import Http404

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
            # Save the existing details first
            serializer.save()

            # Split the incoming service types and areas
            new_service_types = request.data.get('service_type', '').split(',')
            add_service_types = request.data.get('add_service_type', '').split(',')
            new_service_areas = request.data.get('service_area', '').split(',')
            add_service_areas = request.data.get('add_service_area', '').split(',')

            # Clean up whitespace and remove empty entries
            new_service_types = [item.strip() for item in new_service_types if item.strip()]
            add_service_types = [item.strip() for item in add_service_types if item.strip()]
            new_service_areas = [item.strip() for item in new_service_areas if item.strip()]
            add_service_areas = [item.strip() for item in add_service_areas if item.strip()]

            # Combine existing and new service types and areas
            combined_service_types = list(set(new_service_types + add_service_types))
            combined_service_areas = list(set(new_service_areas + add_service_areas))

            # Update the service_provider_details with combined lists
            service_provider_details.service_type = combined_service_types
            service_provider_details.service_area = combined_service_areas
            service_provider_details.save()

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
        # Get the ServiceProviderDetails instance for the authenticated user
        try:
            sp_details = ServiceProviderDetails.objects.get(provider=request.user)
        except ServiceProviderDetails.DoesNotExist:
            return Response({"error": "ServiceProviderDetails not found for this user"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ServiceSerializer(data=request.data)
        if serializer.is_valid():
            # Save the service and link it to the user's ServiceProviderDetails
            service = serializer.save(provider=request.user, sp_details=sp_details)
            return Response(ServiceSerializer(service).data, status=status.HTTP_201_CREATED)
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
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["ServiceProviderBlog"],
        operation_description="Add a new blog",
        manual_parameters=swagger_doccumentation.blog_post_params,
        responses={201: BlogSerializer}
    )
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            blog = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpBlogUpdateAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["ServiceProviderBlog"],
        operation_description="Update an existing blog",
        manual_parameters=swagger_doccumentation.blog_update_params,
        responses={201: BlogSerializer}
    )
    def post(self, request, blog_id):
        blog = get_object_or_404(Blogs, id=blog_id)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
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
        responses={200: 'Delete Successfully'},
    )
    def get(self, request, blog_id):
        blog = get_object_or_404(Blogs, id=blog_id)
        if blog.image:
            os.remove(blog.image.path)
        blog.delete()
        return Response(status=status.HTTP_200_OK)

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
