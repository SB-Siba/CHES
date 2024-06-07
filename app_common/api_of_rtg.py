from django.shortcuts import get_object_or_404
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import FormParser, MultiPartParser
from . import swagger_doccumentation
from django.contrib.auth.hashers import make_password
from .models import ProduceBuy, User, GardeningProfile,UserActivity,SellProduce
from .serializer import (
    CommentSerializer,
    LikeSerializer,
    ProduceBuySerializer,
    GardeningProfileSerializer,
    RateOrderSerializer,
    SellProduceSerializer,
    UpdateProfileSerializer,
    UserProfileSerializer,
    GardeningProfileUpdateRequestSerializer,
    UserActivitySerializer,
    AllActivitiesSerializer
)
from django.contrib.auth import authenticate, login, logout


class UserProfileAPIView(APIView):
    @swagger_auto_schema(
        tags=["user_profile"],
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
        tags=["update_profile"],
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
        tags=["gardening_profile"],
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
        tags=["update_gardening_profile"],
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
        tags=["add_activity"],
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
        tags=["activity_list"],
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
        tags=["sell_produce"],
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
        tags=["sell_produce_list"],
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
        tags=["green_commerce_community_products"],
        operation_description="Community Products API",
        manual_parameters=swagger_doccumentation.green_commerce_product_community_get,
        responses={200: 'Approved sell produces fetched successfully.'}
    )
    def get(self, request):
        produce_obj = SellProduce.objects.exclude(user=request.user).filter(is_approved="approved").order_by("-id")
        serializer = SellProduceSerializer(produce_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BuyingBeginsAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["buy_begins"],
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
        
class BuyBeginsSellerAPIView(APIView):
    @swagger_auto_schema(
        tags=["buy_begins_seller_view"],
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
        tags=["buy_begins_buyer_view"],
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
        tags=["send_payment_link"],
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
        tags=["reject_buy"],
        operation_description="Reject Buy API",
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
        tags=["produce_buy"],
        operation_description="Produce Buy API",
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
        
class AllOrdersAPIView(APIView):
    @swagger_auto_schema(
        tags=["all_orders"],
        operation_description="All Orders API",
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
        tags=["all_posts"],
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
        tags=["Like"],
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

class MinusLikeAPIView(APIView):
    @swagger_auto_schema(
        tags=["Dislike"],
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

class GiveCommentAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["Givecomments"],
        operation_description="Add a comment to a post",
        manual_parameters=swagger_doccumentation.give_comment_post,
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
                "commenter": commenter,
                "comment": comment
            }
            post_obj.comments.append(comment_data)
            post_obj.save()
            return Response({'status': 'Comment added successfully'}, status=status.HTTP_302_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllCommentsAPIView(APIView):
    @swagger_auto_schema(
        tags=["Comments"],
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
    
class RateOrderAPIView(APIView):
    parser_classes = [FormParser, MultiPartParser]
    @swagger_auto_schema(
        tags=["RateOrder"],
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