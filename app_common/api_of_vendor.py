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
from .models import Booking, Order, ProduceBuy, ProductFromVendor, Service, ServiceProviderDetails, VendorDetails, User, GardeningProfile,UserActivity,SellProduce
from .serializer import (
    BlogSerializer,
    BookingSerializer,
    CheckoutFormSerializer,
    CommentSerializer,
    LikeSerializer,
    MessageSerializer,
    OrderUpdateSerializer,
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
from Blogs.models import Blogs


class VendorProfileAPI(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
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
        tags=["All API Vendors"],
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
    

class VendorGardeningProfileAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Gardening Profile API",
        responses={200: GardeningProfileSerializer}
    )
    def get(self, request):
        user = request.user
        try:
            garden_profile_obj = GardeningProfile.objects.get(user=user)
            serializer = GardeningProfileSerializer(garden_profile_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except GardeningProfile.DoesNotExist:
            return Response({'message': 'Gardening profile not found'}, status=status.HTTP_404_NOT_FOUND)

class VendorUpdateGardeningProfileAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Update Gardening Profile API",
        manual_parameters=swagger_doccumentation.update_gardening_profile_post,
        responses={201: 'Update request submitted successfully.'}
    )
    def post(self, request):
        user = request.user
        serializer = GardeningProfileUpdateRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Save the update request
            update_request = serializer.save(user=user)
            return Response({"message": "Update request submitted successfully.", "update_request_id": update_request.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorSellProductAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["All API Vendors"],
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
        tags=["All API Vendors"],
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
        tags=["All API Vendors"],
        operation_description="Get Sell Products List",
        manual_parameters=swagger_doccumentation.sell_product_list_get,
        responses={200: ProductFromVendorSerializer(many=True), 400: "Invalid data provided"},
    )
    def get(self, request):
        user = request.user
        products = ProductFromVendor.objects.filter(vendor=user)
        serializer = ProductFromVendorSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UpdateProductAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Update a product",
        request_body=ProductFromVendorSerializer,
        manual_parameters=swagger_doccumentation.update_product_post,
        responses={200: ProductFromVendorSerializer, 400: "Invalid data provided"},
    )
    def post(self, request, product_id):
        product = get_object_or_404(ProductFromVendor, id=product_id, vendor=request.user)
        serializer = ProductFromVendorSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteSellProductAPIView(APIView):

    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Delete a product",
        manual_parameters=swagger_doccumentation.delete_product_delete,
        responses={204: "Product deleted successfully", 404: "Product not found"},
    )
    def get(self, request, product_id):
        product = get_object_or_404(ProductFromVendor, id=product_id, vendor=request.user)
        product.delete()
        return Response({'success':'Product Deleted Successfully'},status=status.HTTP_204_NO_CONTENT)
    
class ActivityListVendorAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Activity List API",
        manual_parameters=swagger_doccumentation.activity_list_get,
        responses={200: 'List of activities fetched successfully.'}
    )
    def get(self, request):
        activities = UserActivity.objects.filter(user=request.user, is_accepted="approved").order_by('-date_time')
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddActivityRequestVendorAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Add Activity API",
        manual_parameters=swagger_doccumentation.add_activity_request_post,
        responses={201: 'Activity sent for approval successfully.'}
    )
    def post(self, request):
        serializer = UserActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Activity sent for approval successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class VendorSellProduceAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Sell Produce API",
        manual_parameters=swagger_doccumentation.sell_produce_post,
        responses={200: 'Request for sell sent successfully.'}
    )
    def post(self, request):
        serializer = SellProduceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Request for sell sent successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class VendorSellProduceListAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Sell Produce List API",
        manual_parameters=swagger_doccumentation.sell_produces_list_get,
        responses={200: 'List of sell produces fetched successfully.'}
    )
    def get(self, request):
        sel_produces = SellProduce.objects.filter(user=request.user).order_by('-id')
        serializer = SellProduceSerializer(sel_produces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VendorGreenCommerceProductCommunityAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Community Products API",
        manual_parameters=swagger_doccumentation.green_commerce_product_community_get,
        responses={200: 'Approved sell produces fetched successfully.'}
    )
    def get(self, request):
        produce_obj = SellProduce.objects.exclude(user=request.user).filter(is_approved="approved").order_by("-id")
        serializer = SellProduceSerializer(produce_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VendorBuyingBeginsAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Buy Begins API",
        manual_parameters=swagger_doccumentation.buying_begins_post,
        responses={201: 'Purchase initiated successfully.'}
    )
    def post(self, request, prod_id):
        user = request.user
        try:
            buyer = User.objects.get(id=user.id)
            sell_prod_obj = SellProduce.objects.get(id=prod_id)
            seller = sell_prod_obj.user
            product_quantity = sell_prod_obj.product_quantity
            ammount_in_green_points = sell_prod_obj.ammount_in_green_points

            quantity = int(request.data.get('quantity'))

            if product_quantity >= quantity:
                if buyer.wallet >= ammount_in_green_points * quantity:
                    buying_obj = ProduceBuy(
                        buyer=buyer,
                        seller=seller,
                        sell_produce=sell_prod_obj,
                        product_name=sell_prod_obj.product_name,
                        SI_units=sell_prod_obj.SI_units,
                        buying_status='BuyInProgress',
                        quantity_buyer_want=quantity
                    )
                    buying_obj.save()
                    return Response({'message': 'Purchase initiated successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': "You don't have enough green points in your wallet!"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': "The requested amount is not available."}, status=status.HTTP_400_BAD_REQUEST)
        except SellProduce.DoesNotExist:
            return Response({'error': "The product is not available."}, status=status.HTTP_404_NOT_FOUND)
        
class VendorBuyBeginsSellerAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Buy Begins Seller API",
        manual_parameters=swagger_doccumentation.buy_begins_seller_view_get,
        responses={200: ProduceBuySerializer(many=True)}
    )
    def get(self, request):
        user = request.user
        bbeigins_objs = ProduceBuy.objects.filter(seller=user, buying_status="BuyInProgress")
        serializer = ProduceBuySerializer(bbeigins_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VendorBuyBeginsBuyerAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Buy Begins Buyer API",
        manual_parameters=swagger_doccumentation.buy_begins_buyer_view_get,
        responses={200: ProduceBuySerializer(many=True)}
    )
    def get(self, request):
        user = request.user
        bbeigins_objs = ProduceBuy.objects.filter(buyer=user, buying_status="BuyInProgress")
        serializer = ProduceBuySerializer(bbeigins_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class VendorSendPaymentLinkAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Send Payment Link API",
        manual_parameters=swagger_doccumentation.send_payment_link_post,
        responses={200: "Payment link sent successfully."}
    )
    def post(self, request, buy_id):
        try:
            buy_obj = ProduceBuy.objects.get(id=buy_id)
        except ProduceBuy.DoesNotExist:
            return Response({"error": "Buy object not found."}, status=status.HTTP_404_NOT_FOUND)

        ammount_based_on_buyer_quantity = request.data.get('ammount_based_on_buyer_quantity')
        if not ammount_based_on_buyer_quantity:
            return Response({"error": "Amount based on buyer quantity is required."}, status=status.HTTP_400_BAD_REQUEST)

        buy_obj.payment_link = "Send"
        buy_obj.ammount_based_on_quantity_buyer_want = int(ammount_based_on_buyer_quantity)
        buy_obj.save()

        return Response({"message": "Payment link sent successfully."}, status=status.HTTP_200_OK)

class VendorRejectBuyAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Reject Buy Community",
        manual_parameters=swagger_doccumentation.reject_buy_post,
        responses={200: "Buy request rejected successfully."}
    )
    def post(self, request, ord_id):
        try:
            order_obj = ProduceBuy.objects.get(id=ord_id)
        except ProduceBuy.DoesNotExist:
            return Response({"error": "Order object not found."}, status=status.HTTP_404_NOT_FOUND)

        order_obj.buying_status = "BuyRejected"
        order_obj.save()

        return Response({"message": "Buy request rejected successfully."}, status=status.HTTP_200_OK)
    
class VendorProduceBuyAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Community Produce Buy .",
        manual_parameters=swagger_doccumentation.produce_buy_get,
        responses={200: "Purchase completed successfully."}
    )
    def get(self, request, prod_id):
        user = request.user
        try:
            buy_prod_obj = ProduceBuy.objects.get(id=prod_id)
        except ProduceBuy.DoesNotExist:
            return Response({"error": "Produce buy object not found."}, status=status.HTTP_404_NOT_FOUND)

        seller = buy_prod_obj.seller
        buyer = buy_prod_obj.buyer
        ammount_for_quantity_want = buy_prod_obj.ammount_based_on_quantity_buyer_want
        # Check if the amount is 0
        if ammount_for_quantity_want == 0:
            return Response({"error": "Amount for the quantity requested cannot be 0."}, status=status.HTTP_400_BAD_REQUEST)
        sell_prod = buy_prod_obj.sell_produce

        try:
            # Update buyer
            buyer.wallet -= ammount_for_quantity_want
            buyer.total_invest += ammount_for_quantity_want
            buyer.coins += 50

            # Update seller
            seller.wallet += ammount_for_quantity_want
            seller.total_income += ammount_for_quantity_want
            seller.coins += 50

            # Update sell produce
            sell_prod_obj = SellProduce.objects.get(id=sell_prod.id)
            sell_prod_obj.product_quantity -= buy_prod_obj.quantity_buyer_want
            sell_prod_obj.ammount_in_green_points -= ammount_for_quantity_want

            # Update buy product status
            buy_prod_obj.buying_status = "BuyCompleted"

            # Save all objects
            buy_prod_obj.save()
            sell_prod_obj.save()
            buyer.save()
            seller.save()

            return Response({"message": "Purchase completed successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class VendorAllOrdersAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="All Community Orders.",
        manual_parameters=swagger_doccumentation.all_orders_get,
        responses={200: ProduceBuySerializer(many=True)}
    )
    def get(self, request):
        user = request.user
        bbeigins_objs = ProduceBuy.objects.filter(buyer=user)
        serializer = ProduceBuySerializer(bbeigins_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VendorAllPostsAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Retrieve all approved posts with like and comment counts",
        manual_parameters=swagger_doccumentation.all_posts_get,
        responses={200: AllActivitiesSerializer(many=True)}
    )
    def get(self, request):
        posts = UserActivity.objects.filter(is_accepted="approved").order_by("-id")
        serializer = AllActivitiesSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class VendorPlusLikeAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Add a like to a post",
        manual_parameters=swagger_doccumentation.plus_like_get,
        responses={200: 'Give like to a activity'}
    )
    def get(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            activity_id = serializer.validated_data['activity_id']
            activity_obj = UserActivity.objects.get(id=activity_id)
            if user.full_name not in activity_obj.likes:
                activity_obj.likes.append(user.full_name)
                activity_obj.save()
                return Response({'status': 'Like this activity'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorMinusLikeAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Remove a like from a post",
        manual_parameters=swagger_doccumentation.minus_like_get,
        responses={200: 'Remove like from a activity'}
    )
    def get(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            activity_id = serializer.validated_data['activity_id']
            activity_obj = UserActivity.objects.get(id=activity_id)
            if user.full_name in activity_obj.likes:
                activity_obj.likes.remove(user.full_name)
                activity_obj.save()
                return Response({'status': 'Like removed from Activity'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'First like then you have permissions dislike'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorGiveCommentAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Add a comment to a post",
        manual_parameters=swagger_doccumentation.add_comment_post,
        responses={302: 'Comment added successfully'}
    )
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            commenter = request.user.full_name
            comment = serializer.validated_data['comment']
            post_id = serializer.validated_data['post_id']
            post_obj = UserActivity.objects.get(id=post_id)
            comment_data = {
                "id": str(datetime.datetime.now().timestamp()),  # unique ID for the comment
                "commenter": commenter,
                "comment": comment
            }
            post_obj.comments.append(comment_data)
            post_obj.save()
            return Response({'status': 'Comment added successfully'}, status=status.HTTP_302_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDeleteCommentAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Delete a comment from a post",
        manual_parameters=swagger_doccumentation.delete_comment_delete,
        responses={
            204: 'Comment deleted successfully',
            404: 'Comment or post not found'
        }
    )
    def get(self, request, post_id, comment_id, format=None):
        post_obj = get_object_or_404(UserActivity, id=post_id)

        # Find the comment by its ID
        post_obj.comments = [comment for comment in post_obj.comments if comment["id"] != comment_id]

        post_obj.save()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class VendorGetAllCommentsAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Get all comments for a post",
        manual_parameters=swagger_doccumentation.get_all_comments_get,
        responses={200: 'List of comments'}
    )
    def get(self, request):
        post_id = request.data.get('post_id')
        activity_obj = UserActivity.objects.filter(id=post_id).first()
        if activity_obj:
            comments_data = activity_obj.comments
            return Response(comments_data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_404_NOT_FOUND)
    
class VendorRateCommunityOrderAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Rate an community order",
        manual_parameters=swagger_doccumentation.rate_order_post,
        request_body=RateOrderSerializer,
        responses={200: 'Order rated successfully', 400: 'Validation error', 404: 'Order not found'}
    )
    def post(self, request):
        serializer = RateOrderSerializer(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            rating = serializer.validated_data['rating']
            buy_obj = get_object_or_404(ProduceBuy, id=order_id)
            if buy_obj.buying_status == "BuyCompleted":
                seller = buy_obj.seller
                buyer = buy_obj.buyer

                if seller.ratings is None:
                    seller.ratings = []

                new_rating = {
                    "buyer_name": buyer.full_name,
                    "order_product": buy_obj.product_name,
                    "quantity": buy_obj.quantity_buyer_want,
                    "amount_paid": buy_obj.ammount_based_on_quantity_buyer_want,
                    "rating": rating,
                }
                seller.ratings.append(new_rating)
                buy_obj.rating_given = True
                buy_obj.save()
                seller.save()
                return Response({'message': 'Order rated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Order not completed yet or order rejected'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):

    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Order Detail API",
        manual_parameters=swagger_doccumentation.vendor_order_detail_get,
        responses={201: 'Order Detail Fetched Successfully.'}
    )
    def get(self, request, order_uid):
        order = get_object_or_404(Order, uid=order_uid)

        product_list = []
        product_quantity = []
        total_quantity = 0
        grand_total = order.order_meta_data.get('final_cart_value', order.order_meta_data.get('final_value', 0))

        for product_name, quantity in order.products.items():
            product = ProductFromVendor.objects.filter(name=product_name).first()
            product_list.append(product)
            product_quantity.append(quantity)
            total_quantity += int(quantity)
        
        response_data = {
            'order': OrderSerializer(order).data,
            'grand_total': grand_total,
            'products': [{'product': product, 'quantity': quantity} for product, quantity in zip(product_list, product_quantity)],
            'total_quantity': total_quantity,
            'customer_details': order.customer_details
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Order Detail Update API",
        manual_parameters=swagger_doccumentation.vendor_order_detail_post,
        responses={201: 'Order Detail Updated Successfully.'}
    )
    def post(self, request, order_uid):
        order = get_object_or_404(Order, uid=order_uid)
        serializer = OrderUpdateSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VendorFetchUserDetailsAPI(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Fetch user details",
        manual_parameters=swagger_doccumentation.fetch_user_details_get,
        responses={200: "Success"}
    )
    def get(self, request):
        user_id = request.GET.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        user_details = {
            'name': user.full_name,
            'email': user.email,
            'user_image': user.user_image.url if user.user_image else None
        }
        return JsonResponse(user_details)
    
class VendorChatAPI(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Retrieve chat messages",
        responses={200: "Success"}
    )
    def get(self, request):
        messages = Message.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
        sorted_messages = []
        for msg in messages:
            try:
                message_data = json.loads(msg.messages)
                last_message = message_data[-1]
                timestamp = last_message.get('timestamp')
                if timestamp:
                    sorted_messages.append((timestamp, msg))
            except (AttributeError, json.JSONDecodeError, IndexError):
                pass

        sorted_messages = [msg for _, msg in sorted(sorted_messages, key=lambda x: x[0], reverse=True)]

        user_last_message = []
        for message in sorted_messages:
            try:
                message_data = json.loads(message.messages)  # Assuming `message.messages` contains JSON data
                last_message = message_data[-1]
                timestamp = timezone.localtime(timezone.datetime.strptime(last_message['timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z"))
                formatted_time = timestamp.strftime("%I:%M %p")
                user_last_message.append((last_message['message'], formatted_time))
            except (json.JSONDecodeError, IndexError, KeyError):
                pass

        # zipped_messages = zip(sorted_messages, user_last_message)

        # Serialize the zipped messages using MessageSerializer
        serialized_messages = MessageSerializer(sorted_messages, many=True)

        context = {'zipped_messages': serialized_messages.data,'last_message':user_last_message}
        return Response(context)

class VendorStartMessagesAPI(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Start a new message conversation",
        manual_parameters=swagger_doccumentation.start_message_post,
        request_body=StartMessagesSerializer,
        responses={
            201: "Message started successfully",
            400: "Message already exists",
            404: "Receiver not found"
        }
    )
    def post(self, request, r_id):
        receiver = get_object_or_404(User, pk=r_id)
        serializer = StartMessagesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_name = serializer.validated_data.get('product_name', "None")
        
        initial_message = (
            f"Hi {receiver.full_name}, I am interested in purchasing {product_name}."
            if product_name != "None"
            else f"Hi {receiver.full_name}, I would like to start a conversation with you."
        )
        sender = request.user

        if Message.objects.filter(sender=sender, receiver=receiver).exists():
            return Response({"detail": "Message already exists."}, status=400)

        message_data = {
            'sender': sender.id,
            'message': initial_message,
            'timestamp': timezone.now().isoformat(),
        }
        messages_json = json.dumps([message_data])
        msg_obj = Message(sender=sender, receiver=receiver, message_status="Start", messages=messages_json)
        msg_obj.save()

        return Response({"detail": "Message started successfully."}, status=201)

class VendorSendMessageApi(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Send a message",
        manual_parameters=swagger_doccumentation.send_message_post,
        request_body=SendMessageSerializer,
        responses={201: "Message sent successfully"}
    )
    def post(self,request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        receiver = get_object_or_404(User, pk=receiver_id)
        message = request.data.get('message')

        existing_messages = Message.objects.filter(Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)).values_list('messages', flat=True)
        messages = json.loads(existing_messages[0]) if existing_messages and existing_messages[0] is not None else []

        message_data = {
            'sender': sender.id,
            'message': message,
            'timestamp': timezone.now().isoformat(),
        }
        messages.append(message_data)

        messages_to_update = Message.objects.filter(Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
        for message in messages_to_update:
            message.messages = json.dumps(messages)
            message.is_read = False
            message.save()

        return Response({"detail": "Message sent successfully."}, status=201)

class VendorFetchMessageApi(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        operation_description="Fetch messages between users",
        manual_parameters=swagger_doccumentation.fetch_messages_get,
        responses={200: "Success"}
    )
    def get(self,request):
        receiver_id = request.GET.get('receiver_id')
        receiver = get_object_or_404(User, pk=receiver_id)
        messages = Message.objects.filter(Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user)).values_list('messages', flat=True)

        f_messages = [msg for msg in messages if msg is not None]
        for message in Message.objects.filter(Q(receiver=request.user) | Q(sender=request.user)):
            try:
                messages_dict = json.loads(message.messages)
                last_message_index = len(messages_dict) - 1
                last_message = messages_dict[last_message_index]
                if int(last_message['sender']) == request.user.id:
                    message.is_read = True
                else:
                    message.is_read = False
                message.save()
            except:
                pass

        sender_id = request.user.id
        response_data = {
            'messages': json.loads(messages[0]) if f_messages else [],
            'senderId': sender_id
        }
        return JsonResponse(response_data, safe=False)
    
class VendorServiceProvidersListAPIView(APIView):
    @swagger_auto_schema(
        tags=["All API Vendors"],
        manual_parameters=swagger_doccumentation.service_provider_list_get,
        operation_description="Get a list of approved service providers",
        responses={200: ServiceProviderSerializer(many=True)}
    )
    def get(self, request):
        service_providers = ServiceProviderDetails.objects.filter(provider__is_approved=True)
        serializer = ServiceProviderSerializer(service_providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
# ####################### Blog

class VendorBlogListAPIView(APIView):
    @swagger_auto_schema(
        tags=["VendorBlog"],
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
        blog_list = Blogs.objects.filter(user=request.user).order_by('-id')
        serializer = BlogSerializer(blog_list, many=True)
        return Response(serializer.data)

class VendorBlogAddAPIView(APIView):
    @swagger_auto_schema(
        tags=["VendorBlog"],
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
        ]
    )
    def post(self, request):
        serializer = BlogSerializer(data=request.data, files=request.FILES)
        if serializer.is_valid():
            blog = serializer.save(user=request.user)
            return Response(BlogSerializer(blog).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorBlogUpdateAPIView(APIView):
    @swagger_auto_schema(
        tags=["VendorBlog"],
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

class VendorBlogDeleteAPIView(APIView):
    @swagger_auto_schema(
        tags=["VendorBlog"],
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
            image_path = blog.image.path
            os.remove(image_path)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VendorBlogViewAPIView(APIView):
    @swagger_auto_schema(
        tags=["VendorBlog"],
        operation_description="Retrieve a list of approved blogs",
        responses={200: BlogSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request):
        blogs = Blogs.objects.filter(is_accepted="approved")
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

class VendorBlogDetailsAPIView(APIView):
    @swagger_auto_schema(
        tags=["VendorBlog"],
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

class VendorBlogSearchAPIView(APIView):
    @swagger_auto_schema(
        tags=["VendorBlog"],
        operation_description="Search for blogs",
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer <token>", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('query', openapi.IN_QUERY, description="Search query", type=openapi.TYPE_STRING),
            openapi.Parameter('filter_by', openapi.IN_QUERY, description="Filter by field", type=openapi.TYPE_STRING)
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
        else:
            blogs = Blogs.objects.none()  # Empty queryset if filter_by is invalid
        
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)