import datetime
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
from .models import Booking, Order, ProduceBuy, ProductFromVendor, Service, VendorDetails, User, GardeningProfile,UserActivity,SellProduce
from .serializer import (
    BookingSerializer,
    CheckoutFormSerializer,
    CommentSerializer,
    LikeSerializer,
    MessageSerializer,
    ProduceBuySerializer,
    GardeningProfileSerializer,
    ProductFromVendorSerializer,
    RateOrderSerializer,
    SellProduceSerializer,
    SendMessageSerializer,
    ServiceProviderSerializer,
    ServiceSerializer,
    StartMessagesSerializer,
    UpdateProfileSerializer,
    UserProfileSerializer,
    GardeningProfileUpdateRequestSerializer,
    UserActivitySerializer,
    AllActivitiesSerializer,
    VendorSerializer,
    VendorDetailsSerializer
)
from user_dashboard.serializers import DirectBuySerializer,OrderSerializer
from django.contrib.auth import authenticate, login, logout
import json
from django.db.models import Q
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.utils import timezone

class VendorProfileAPI(APIView):
    @swagger_auto_schema(
        tags=["vendorprofile"],
        operation_description="Retrieve Vendor Profile",
        manual_parameters=swagger_doccumentation.vendor_profile_get,
        responses={200: VendorSerializer(many=False)}
    )
    def get(self, request):
        user = request.user
        vendor_obj = get_object_or_404(VendorDetails, vendor=user)
        serializer = VendorSerializer(vendor_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VendorUpdateProfileAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["vendor"],
        operation_description="Update Vendor Profile",
        request_body=VendorDetailsSerializer,
        manual_parameters=swagger_doccumentation.vendor_update_profile_post,
        responses={200: "Profile updated successfully", 400: "Invalid data provided"},
    )
    def post(self, request):
        vendor_details = get_object_or_404(VendorDetails, vendor=request.user)
        serializer = VendorDetailsSerializer(instance=vendor_details, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update user object if needed
            user_obj = request.user
            if 'image' in request.FILES:
                user_obj.user_image = request.FILES['image']
            user_obj.save()

            return Response("Profile updated successfully", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendorSellProductAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["vendorsellproduct"],
        operation_description="Vendor Sell Product",
        request_body=ProductFromVendorSerializer,
        manual_parameters=swagger_doccumentation.vendor_sell_product_post,
        responses={200: "Product sell request sent successfully", 400: "Invalid data provided"},
    )
    def post(self, request):
        serializer = ProductFromVendorSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save(commit=False)
            product.vendor = request.user
            product.save()

            return Response("Product sell request sent successfully", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendorSoldProductsAPIView(APIView):

    @swagger_auto_schema(
        tags=["vendor"],
        operation_description="Get Vendor Sold Products",
        manual_parameters=swagger_doccumentation.vendor_sold_product_get,
        responses={200: OrderSerializer(many=True), 400: "Invalid data provided"},
    )
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(vendor=user)
        order_list = []
        product_list = []
        quantity_list = []

        for order in orders:
            order_list.append(order)
            products = []
            quantity = []
            for product, qty in order.products.items():
                products.append(product)
                quantity.append(qty)
            product_list.append(products)
            quantity_list.append(quantity)
        
        data = {
            'order_list': OrderSerializer(order_list, many=True).data,
            'product_list': product_list,
            'quantity_list': quantity_list,
        }
        return Response(data, status=status.HTTP_200_OK)

class SellProductsListAPIView(APIView):

    @swagger_auto_schema(
        tags=["vendor"],
        operation_description="Get Sell Products List",
        manual_parameters=swagger_doccumentation.sell_product_list_get,
        responses={200: ProductFromVendorSerializer(many=True), 400: "Invalid data provided"},
    )
    def get(self, request):
        user = request.user
        products = ProductFromVendor.objects.filter(vendor=user)
        serializer = ProductFromVendorSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)