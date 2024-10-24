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
from django.db.models.functions import Lower
from django.contrib.auth.hashers import make_password
from .models import Booking, CategoryForServices, Order, ProduceBuy, ProductFromVendor, Service, ServiceProviderDetails, User, GardeningProfile,UserActivity,SellProduce,CategoryForProduces
from django.utils.dateparse import parse_datetime
from .serializer import (
    BookingSerializer,
    CategoryForProducesSerializer,
    CategoryForServieProviderSerializer,
    CheckoutFormSerializer,
    CommentSerializer,
    MessageSerializer,
    ProduceBuySerializer,
    GardeningProfileSerializer,
    ProductFromVendorSerializer,
    RateOrderSerializer,
    SellProduceSerializer,
    SendMessageSerializer,
    ServiceDetailsSerializer,
    ServiceProviderSerializer,
    ServiceSerializer,
    StartMessagesSerializer,
    UpdateProfileSerializer,
    UserProfileSerializer,
    GardeningProfileUpdateRequestSerializer,
    UserActivitySerializer,
    AllActivitiesSerializer,
    BlogSerializer,
    UserQuerySerializer,
)
from django.utils.timezone import make_aware
from user_dashboard.serializers import DirectBuySerializer,OrderSerializer
from django.contrib.auth import authenticate, login, logout
import json
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from Blogs.models import Blogs


class UserProfileAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="User Profile API",
        manual_parameters=swagger_doccumentation.user_profile_get,
        responses={200: UserProfileSerializer}
    )
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileViewAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Update Profile API",
        manual_parameters=swagger_doccumentation.update_profile_post,
        responses={200: 'Profile updated successfully'}
    )
    def post(self, request):
        user = request.user
        serializer = UpdateProfileSerializer(user, data=request.data)

        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            if password:
                serializer.validated_data['password'] = make_password(password)  # Hash the password
            serializer.save()  # Save the updated profile
            return Response({'message': 'Your profile has been updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GardeningProfileAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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

class UpdateGardeningProfileAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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
        
class AddActivityRequestAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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

class ActivityListAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Activity List API",
        manual_parameters=swagger_doccumentation.activity_list_get,
        responses={200: 'List of activities fetched successfully.'}
    )
    def get(self, request):
        activities = UserActivity.objects.filter(user=request.user, is_accepted="approved").order_by('-date_time')
        serializer = UserActivitySerializer(activities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SellProduceAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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
        
class SellProduceListAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Sell Produce List API",
        manual_parameters=swagger_doccumentation.sell_produces_list_get,
        responses={200: 'List of sell produces fetched successfully.'}
    )
    def get(self, request):
        sel_produces = SellProduce.objects.filter(user=request.user).order_by('-id')
        serializer = SellProduceSerializer(sel_produces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GreenCommerceProductCommunityAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Fetch community products with optional filtering by category or search query.",
        manual_parameters=swagger_doccumentation.green_commerce_product_community_get,
        responses={200: 'Approved sell produces fetched successfully.'}
    )
    def get(self, request):
        try:
            # Get search query and category from request parameters
            search_query = request.GET.get('search_query', '')
            selected_category = request.GET.get('category')
            
            # Fetch approved produce items excluding those from the current user
            produce_query = SellProduce.objects.exclude(user=request.user).filter(is_approved="approved")
            # Apply filtering based on category
            if selected_category and selected_category != 'all':
                produce_query = produce_query.filter(produce_category=selected_category)

            # Apply filtering based on search query
            if search_query:
                produce_query = produce_query.filter(product_name__icontains=search_query)

            # Order the results by latest date
            produce_obj = produce_query.order_by("-date_time")
            # Serialize the data
            serializer = SellProduceSerializer(produce_obj, many=True)

            # Return serialized data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BuyingBeginsAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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
            amount_in_green_points = sell_prod_obj.amount_in_green_points

            quantity = int(request.data.get('quantity'))

            if product_quantity >= quantity:
                if buyer.wallet >= amount_in_green_points * quantity:
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
        
class BuyBeginsSellerAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Buy Begins Seller API",
        manual_parameters=swagger_doccumentation.buy_begins_seller_view_get,
        responses={200: ProduceBuySerializer(many=True)}
    )
    def get(self, request):
        user = request.user
        bbeigins_objs = ProduceBuy.objects.filter(seller=user, buying_status="BuyInProgress")
        serializer = ProduceBuySerializer(bbeigins_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BuyBeginsBuyerAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Buy Begins Buyer API",
        manual_parameters=swagger_doccumentation.buy_begins_buyer_view_get,
        responses={200: ProduceBuySerializer(many=True)}
    )
    def get(self, request):
        user = request.user
        bbeigins_objs = ProduceBuy.objects.filter(buyer=user, buying_status="BuyInProgress")
        serializer = ProduceBuySerializer(bbeigins_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SendPaymentLinkAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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

class RejectBuyAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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
    
class ProduceBuyAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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
            sell_prod_obj.amount_in_green_points -= ammount_for_quantity_want

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
        
class AllOrdersAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="All Community Orders.",
        manual_parameters=swagger_doccumentation.all_orders_get,
        responses={200: ProduceBuySerializer(many=True)}
    )
    def get(self, request):
        user = request.user
        bbeigins_objs = ProduceBuy.objects.filter(buyer=user)
        serializer = ProduceBuySerializer(bbeigins_objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllPostsAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Retrieve all approved posts with like and comment counts",
        manual_parameters=swagger_doccumentation.all_posts_get,
        responses={200: AllActivitiesSerializer(many=True)}
    )
    def get(self, request):
        posts = UserActivity.objects.filter(is_accepted="approved").order_by("-id")
        serializer = AllActivitiesSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlusLikeAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Add a like to a post",
        manual_parameters=swagger_doccumentation.plus_like_get,
        responses={200: 'Give like to a activity'}
    )
    def get(self, request):
        user = request.user
        activity_id = request.GET.get('activity_id')
        print(activity_id,type(activity_id))
        activity_obj = UserActivity.objects.get(id=activity_id)
        if user.full_name not in activity_obj.likes:
            activity_obj.likes.append(user.full_name)
            activity_obj.save()
            return Response({'status': 'Like this activity'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

class MinusLikeAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Remove a like from a post",
        manual_parameters=swagger_doccumentation.minus_like_get,
        responses={200: 'Remove like from a activity'}
    )
    def get(self, request):
        user = request.user
        activity_id = request.GET.get('activity_id')
        print(activity_id,type(activity_id))
        activity_obj = UserActivity.objects.get(id=activity_id)
        if user.full_name in activity_obj.likes:
            activity_obj.likes.remove(user.full_name)
            activity_obj.save()
            return Response({'status': 'Like removed from Activity'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'First like then you have permissions dislike'}, status=status.HTTP_400_BAD_REQUEST)

class GiveCommentAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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
                "comment": comment,
                'commenter_id':request.user.id
            }
            post_obj.comments.append(comment_data)
            post_obj.save()
            return Response({'status': 'Comment added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCommentAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Delete a comment from a post",
        manual_parameters=swagger_doccumentation.delete_comment_delete,
        responses={
            200: 'Comment deleted successfully',
            404: 'Comment or post not found'
        }
    )
    def get(self, request, post_id, comment_id, format=None):
        post_obj = get_object_or_404(UserActivity, id=post_id)

        # Find the comment by its ID
        post_obj.comments = [comment for comment in post_obj.comments if comment["id"] != comment_id]

        post_obj.save()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_200_OK)

class GetAllCommentsAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Get all comments for a post",
        manual_parameters=swagger_doccumentation.get_all_comments_get,
        responses={200: 'List of comments'}
    )
    def get(self, request):
        post_id = request.GET.get('post_id')
        print(f"Post Id : {post_id}")
        activity_obj = UserActivity.objects.filter(id=post_id).first()
        if activity_obj:
            comments_data = activity_obj.comments

            # Assume comments_data is a list of dictionaries with a 'commenter_id' field
            for comment in comments_data:
                # Assuming the comment data contains 'commenter_id' field that holds the user ID of the commenter
                is_commenter = comment.get('commenter_id') == request.user.id
                comment['is_commenter'] = is_commenter  # Add this flag to the comment data

            return Response(comments_data, status=status.HTTP_200_OK)

        return Response([], status=status.HTTP_404_NOT_FOUND)
    
class RateOrderAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Rate an order",
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

class VendorsProductsAPI(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Product from vendors",
        responses={
            200: openapi.Response(
                description="All Vendor Products",
                schema=ProductFromVendorSerializer(many=True)  # Explicitly define the response schema
            ),
            400: 'Validation error',
            404: 'Vendor Products not found'
        }
    )
    def get(self, request):
        products = ProductFromVendor.objects.all().order_by("-id")
        serializer = ProductFromVendorSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
class FetchUserDetailsAPI(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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

class ChatAPI(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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

        # zipped_messages = zip(sorted_messages, user_last_message)

        # Serialize the zipped messages using MessageSerializer
        serialized_messages = MessageSerializer(sorted_messages, many=True)

        context = {'zipped_messages': serialized_messages.data}
        return Response(context)

class StartMessagesAPI(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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

class SendMessageApi(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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

class FetchMessageApi(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
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
    
class ServiceProvidersListAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        manual_parameters=swagger_doccumentation.service_provider_list_get,
        operation_description="Get a list of approved service providers",
        responses={200: ServiceProviderSerializer(many=True)}
    )
    def get(self, request):
        service_providers = ServiceProviderDetails.objects.filter(provider__is_approved=True)
        serializer = ServiceProviderSerializer(service_providers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CheckoutAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Fetch order details",
        manual_parameters=swagger_doccumentation.checkout_get,
        responses={200: 'Success', 404: 'Not Found'}
    )
    def get(self, request, vprod_id, vendor_email):
        user = request.user
        offer_discount = request.data.get('offer_discount', None)
        print(offer_discount)
        vendor_product_obj = get_object_or_404(ProductFromVendor, id=vprod_id)
        serializer = DirectBuySerializer(vendor_product_obj, context={'offer_discount': offer_discount})
        order_details = serializer.data

        ord_meta_data = {}
        for i, j in order_details.items():
            ord_meta_data.update(j)

        data = {
            "vendor_product": vendor_product_obj.name,
            "gross_amount": round(ord_meta_data['gross_value'], 2),
            "our_price": round(ord_meta_data['our_price'], 2),
            "discount_amount": '{:.2f}'.format(ord_meta_data['discount_amount']),
            "discount_percentage": round(ord_meta_data['discount_percentage'], 2),
            "gst": '{:.2f}'.format(float(ord_meta_data['charges']["GST"])),
            "total": round(ord_meta_data['final_value'], 2),
            "offer_discount": offer_discount,
            "delivery_charge": float(ord_meta_data['charges']["Delivary"]),
        }
        return JsonResponse(data, safe=False)

    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Place an order",
        request_body=CheckoutFormSerializer,
        manual_parameters=swagger_doccumentation.checkout_post,
        responses={200: 'Order Successful!', 400: 'Error while placing Order'}
    )
    def post(self, request, vprod_id, vendor_email):
        serializer = CheckoutFormSerializer(data=request.data)
        offer_discount = request.data.get('offer_discount', None)
        
        if serializer.is_valid():
            user = request.user
            customer_details = serializer.validated_data
            
            prod_obj = get_object_or_404(ProductFromVendor, id=vprod_id)
            serializer = DirectBuySerializer(prod_obj, context={'offer_discount': offer_discount})
            order_details = serializer.data
            ord_meta_data = {}
            for i, j in order_details.items():
                ord_meta_data.update(j)
            t_price = round(ord_meta_data['final_value'], 2)

            try:
                vendor = get_object_or_404(User, email=vendor_email)
                order = Order(
                    customer=user,
                    vendor=vendor,
                    products={prod_obj.name: 1},
                    order_value=t_price,
                    customer_details=customer_details,
                    order_meta_data=ord_meta_data
                )

                if int(offer_discount) == 1:
                    user.wallet -= float(prod_obj.green_coins_required)
                    vendor.wallet += float(prod_obj.green_coins_required)
                    user.save()
                    vendor.save()

                order.save()
                prod_obj.stock -= 1
                prod_obj.save()
                return Response({"detail": "Order Successful!"}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"detail": "Error while placing Order."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllOrdersFromVendorsApi(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="See all orders",
        manual_parameters=swagger_doccumentation.orders_from_vendors_parameters,
        responses={200: OrderSerializer(many=True)}
    )
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(customer=user).order_by("-uid")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class RateOrderFromVendorApi(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Rate an order from a vendor",
        request_body=RateOrderSerializer,
        manual_parameters=swagger_doccumentation.rate_order_post,
        responses={
            200: "Rating submitted successfully",
            400: "Validation error",
            404: "Order or product not found",
            409: "Rating already given for this order"
        }
    )
    def post(self, request):
        serializer = RateOrderSerializer(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            rating = serializer.validated_data['rating']
            
            buy_obj = get_object_or_404(Order, id=order_id)

            if buy_obj.rating_given:
                return Response({"detail": "Rating already given for this order"}, status=status.HTTP_409_CONFLICT)
            
            vendor = buy_obj.vendor
            customer = buy_obj.customer
            product = ""
            
            for i, j in buy_obj.products.items():
                product = i
            
            product_obj = get_object_or_404(ProductFromVendor, name=product)
            
            if product_obj.ratings is None:
                product_obj.ratings = []

            new_rating = {
                "buyer_name": customer.full_name,
                "order_product": product,
                "amount_paid": buy_obj.order_value,
                "rating": rating,
            }
            
            product_obj.ratings.append(new_rating)
            buy_obj.rating_given = True
            buy_obj.save()
            product_obj.save()
            
            return Response({"detail": "Rating submitted successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# #################################### BLOGS

class BlogListAPIView(APIView):
    @swagger_auto_schema(
        tags=["RTGBlog"],
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

class BlogAddAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["RTGBlog"],
        operation_description="Add a new blog",
        manual_parameters=swagger_doccumentation.blog_post_params,
        responses={201: BlogSerializer}
    )
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            blog = serializer.save(user=request.user)
            return Response(BlogSerializer(blog).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogUpdateAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]

    @swagger_auto_schema(
        tags=["RTGBlog"],
        operation_description="update blog",
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

class BlogDeleteAPIView(APIView):
    @swagger_auto_schema(
        tags=["RTGBlog"],
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

class BlogViewAPIView(APIView):
    @swagger_auto_schema(
        tags=["RTGBlog"],
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

class BlogDetailsAPIView(APIView):
    @swagger_auto_schema(
        tags=["RTGBlog"],
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

# Services

# class ListOfServicesByServiceProvidersAPIView(APIView):
#     @swagger_auto_schema(
#         tags=["Roof Top Gardeners"],
#         operation_description="List Of Services By Service Provider",
#         manual_parameters=swagger_doccumentation.list_services_params,
#         responses={201: ServiceSerializer(many=True)}
#     )
#     def get(self, request):
#         try:
#             services = Service.objects.all()
#             serializer = ServiceSerializer(services, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.exceptions import NotFound

class ListOfServicesByServiceProvidersAPIView(APIView):
    """
    API view to list all categories or services under a selected category.
    """
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="List Services by Category",
        manual_parameters=swagger_doccumentation.list_services_params,
        responses={200: ServiceSerializer(many=True)}
    )
    def get(self, request):
        try:
            # Get the category ID from query parameters
            category_id = request.query_params.get('category_id')

            if category_id:
                # If a category is selected, return the services within that category
                try:
                    selected_category = CategoryForServices.objects.get(id=category_id)
                except CategoryForServices.DoesNotExist:
                    raise NotFound(detail="Category not found")

                services = Service.objects.filter(service_type=selected_category)
                serializer = ServiceSerializer(services, many=True)
                return Response({'services': serializer.data, 'selected_category': selected_category.service_category}, status=status.HTTP_200_OK)
            else:
                # If no category is selected, return the list of categories
                categories = CategoryForServices.objects.all()
                category_serializer = CategoryForServieProviderSerializer(categories, many=True)
                return Response({'categories': category_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ServiceSearchAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Search Services",
        manual_parameters=swagger_doccumentation.service_search_params,
        responses={200: ServiceSerializer(many=True)}
    )
    def get(self, request):
        try:
            search_query = request.GET.get('search_query')
            if search_query:
                search_query_lower = search_query.lower()
                services = Service.objects.annotate(
                    name_lower=Lower('name'),
                    service_type_lower=Lower('service_type')
                ).filter(
                    Q(name_lower__icontains=search_query_lower) |
                    Q(service_type_lower__icontains=search_query_lower)
                )
            else:
                services = Service.objects.all()

            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ServiceDetailsAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Get details of a service",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                required=True,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'service_id',
                openapi.IN_PATH,
                description="ID of the service",
                required=True,
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            200: ServiceDetailsSerializer,
            404: openapi.Response('Service not found'),
            400: openapi.Response('Error occurred')
        }
    )
    def get(self, request, service_id):
        try:
            service = get_object_or_404(Service, id=service_id)
            serializer = ServiceDetailsSerializer(service)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Book a service",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer <token>",
                required=True,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'service_id',
                openapi.IN_PATH,
                description="ID of the service",
                required=True,
                type=openapi.TYPE_INTEGER
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'booking_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Date of booking'),
                'booking_time': openapi.Schema(type=openapi.TYPE_STRING, format='time', description='Time of booking'),
            },
            required=['booking_date', 'booking_time']
        ),
        responses={
            201: openapi.Response('Booking created successfully'),
            400: openapi.Response('Error occurred')
        }
    )
    def post(self, request, service_id):
        try:
            service = get_object_or_404(Service, id=service_id)
            
            if Booking.objects.filter(service=service, gardener=request.user).exists():
                return Response({'error': 'Booking already exists'}, status=status.HTTP_400_BAD_REQUEST)

            # Extract booking date and time from request data
            booking_date_str = request.data.get('booking_date')
            booking_time_str = request.data.get('booking_time')

            # Combine date and time into a single datetime object
            booking_datetime_str = f"{booking_date_str}T{booking_time_str}"
            booking_date = parse_datetime(booking_datetime_str)

            # Make the datetime timezone-aware if it's not already
            if booking_date and not booking_date.tzinfo:
                booking_date = make_aware(booking_date)

            if not booking_date:
                return Response({'error': 'Invalid date or time format'}, status=status.HTTP_400_BAD_REQUEST)

            # Create and save the booking
            booking = Booking(
                service=service,
                gardener=request.user,
                booking_date=booking_date
            )
            booking.save()
            return Response({'status': 'Booking created successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MyBookedServicesAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="My Booked Services",
        manual_parameters=swagger_doccumentation.my_booked_services_params,
        responses={200: BookingSerializer(many=True)}
    )
    def get(self, request):
        try:
            booked_services = Booking.objects.filter(gardener=request.user).exclude(status="declined")
            serializer = BookingSerializer(booked_services, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeclineBookingAPIView(APIView):
    @swagger_auto_schema(
        tags=["Roof Top Gardeners"],
        operation_description="Decline a Booking",
        manual_parameters=swagger_doccumentation.decline_booking_params,
        responses={
            200: openapi.Response('Booking declined successfully'),
            404: openapi.Response('Booking not found'),
            400: openapi.Response('Error occurred')
        }
    )
    def get(self, request, booking_id):
        try:
            booking = get_object_or_404(Booking, id=booking_id)
            if request.user == booking.gardener:
                booking.status = 'declined'
                booking.save()
                return Response({'status': 'Booking declined successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# User Query

class UserQueryCreateView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Submit Query"],
        operation_description="Submit a user query",
        manual_parameters=swagger_doccumentation.user_query_post,
        responses={201: 'Query created successfully', 400: 'Invalid data'}
    )
    def post(self, request, *args, **kwargs):
        serializer = UserQuerySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

# all categpries

class CategoryForProducesListView(APIView):
    @swagger_auto_schema(
        tags=["Produces Categories"],
        operation_description="All Categories Of Produces.",
        responses={200: CategoryForProducesSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        categories = CategoryForProduces.objects.all()
        serializer = CategoryForProducesSerializer(categories, many=True)
        return Response(serializer.data)
    

class CategoryForServiceProviderListView(APIView):
    @swagger_auto_schema(
        tags=["ServiceProvider Categories"],
        operation_description="All Categories Of ServiceProvider.",
        responses={200: CategoryForServieProviderSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        categories = CategoryForServices.objects.all()
        serializer = CategoryForServieProviderSerializer(categories, many=True)
        return Response(serializer.data)