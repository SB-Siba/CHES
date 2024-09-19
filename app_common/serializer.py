from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    Booking,
    Order,
    ProduceBuy,
    ProductFromVendor,
    SellProduce,
    Service,
    User, 
    GardeningProfile, 
    GaredenQuizModel, 
    VendorDetails, 
    ServiceProviderDetails,
    GardeningProfileUpdateRequest,
    UserActivity
)
from chatapp.models import Message
from django.db.models import Q
from Blogs.models import Blogs

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    is_rtg = serializers.BooleanField(required=False)
    is_vendor = serializers.BooleanField(required=False)
    is_serviceprovider = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'confirm_password', 'contact', 'city', 'is_rtg', 'is_vendor', 'is_serviceprovider']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        user = User(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            contact=validated_data['contact'],
            city=validated_data['city'],
        )
        user.set_password(validated_data['password'])
        if validated_data.get('is_rtg'):
            user.is_rtg = True
        if validated_data.get('is_vendor'):
            user.is_vendor = True
        if validated_data.get('is_serviceprovider'):
            user.is_serviceprovider = True
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user and user.is_active:
            data['user'] = user
        else:
            raise serializers.ValidationError('Invalid credentials or inactive account')
        return data

class GardeningProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GardeningProfile
        fields = ['garden_area', 'number_of_plants', 'number_of_unique_plants', 'garden_image']

class GardeningQuizSerializer(serializers.Serializer):
    q1 = serializers.CharField(required=True)
    q2 = serializers.CharField(required=True)
    q3 = serializers.CharField(required=True)
    q4 = serializers.CharField(required=True)
    q5 = serializers.CharField(required=True)

class GardeningQuizDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GaredenQuizModel
        fields = ['questionANDanswer']

class GardeningQuizQuestionSerializer(serializers.Serializer):
    q1 = serializers.CharField(read_only=True, default='What is the process of cutting off dead or overgrown branches called?')
    q2 = serializers.CharField(read_only=True, default='Which of the following is a perennial flower?')
    q3 = serializers.CharField(read_only=True, default='What is the best time of day to water plants?')
    q4 = serializers.CharField(read_only=True, default='Which type of soil holds water the best?')
    q5 = serializers.CharField(read_only=True, default='What is the primary purpose of adding compost to soil?')


class VendorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDetails
        fields = ['business_name', 'business_address', 'business_description', 'business_license_number', 'business_category', 'establishment_year', 'website', 'established_by']

class ServiceProviderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderDetails
        fields = ['service_type', 'service_area', 'average_cost_per_hour', 'years_experience']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'contact', 'address', 'city', 'quiz_score', 'user_image',
                  'is_rtg', 'is_vendor', 'is_serviceprovider', 'wallet', 'coins', 'ratings', 'facebook_link',
                  'instagram_link', 'twitter_link', 'youtube_link']

    def calculate_avg_rating(self, ratings):
        total_rating = sum(float(rating['rating']) for rating in ratings)
        num_ratings = len(ratings)
        avg_rating = total_rating / num_ratings if num_ratings > 0 else 0
        return round(avg_rating, 2)

    def to_representation(self, instance):
        # Include rating_of_user field in the serialized data
        rating_of_user = self.calculate_avg_rating(instance.ratings)
        representation = super().to_representation(instance)
        representation['rating_of_user'] = rating_of_user
        return representation

class UpdateProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)  # To handle password update

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'contact',
            'facebook_link',
            'instagram_link',
            'twitter_link',
            'youtube_link',
            'address',
            'user_image',
            'password',  # Include password field for updating password
        ]

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.email = validated_data.get('email', instance.email)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.facebook_link = validated_data.get('facebook_link', instance.facebook_link)
        instance.instagram_link = validated_data.get('instagram_link', instance.instagram_link)
        instance.twitter_link = validated_data.get('twitter_link', instance.twitter_link)
        instance.youtube_link = validated_data.get('youtube_link', instance.youtube_link)
        instance.address = validated_data.get('address', instance.address)
        instance.user_image = validated_data.get('user_image', instance.user_image)
        
        # Update password if provided
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class GardeningProfileUpdateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GardeningProfileUpdateRequest
        fields = ['garden_area', 'number_of_plants', 'number_of_unique_plants', 'garden_image']

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['activity_title', 'activity_content', 'activity_image']

class SellProduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellProduce
        fields = '__all__'

class ProduceBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduceBuy
        fields = [
            'id',
            'buyer',
            'seller',
            'sell_produce',
            'product_name',
            'SI_units',
            'buying_status',
            'quantity_buyer_want',
            'date_time'
        ]
        read_only_fields = ['id', 'buyer', 'seller', 'sell_produce', 'product_name', 'SI_units', 'buying_status', 'date_time']


class SendPaymentLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduceBuy
        fields = ['ammount_based_on_quantity_buyer_want']
        extra_kwargs = {
            'ammount_based_on_quantity_buyer_want': {'required': True}
        }

class RejectBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduceBuy
        fields = ['buying_status']
        extra_kwargs = {
            'buying_status': {'required': True, 'default': 'BuyRejected'}
        }

class AllActivitiesSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    user_liked = serializers.SerializerMethodField()

    class Meta:
        model = UserActivity
        fields = ['id', 'is_accepted', 'likes', 'comments', 'like_count', 'comment_count', 'user_liked','activity_image','activity_title','activity_content']

    def get_like_count(self, obj):
        return len(obj.likes)

    def get_comment_count(self, obj):
        return len(obj.comments)

    def get_user_liked(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user.full_name in obj.likes
        return False


class CommentSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    comment = serializers.CharField(max_length=1000)

class RateOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    rating = serializers.FloatField(required=True, min_value=0, max_value=5)

class ProductFromVendorSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(source='calculate_avg_rating', read_only=True)
    discounted_price = serializers.DecimalField(source='calculate_discounted_price', max_digits=10, decimal_places=2, read_only=True)
    has_message = serializers.SerializerMethodField()

    class Meta:
        model = ProductFromVendor
        fields = [
            'id', 'vendor', 'name', 'description', 'discount_price', 'max_price',
            'image', 'stock', 'category', 'reason', 'green_coins_required',
            'discount_percentage', 'ratings', 'average_rating', 'discounted_price', 'has_message'
        ]

    def get_has_message(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            msg_obj = Message.objects.filter(Q(receiver=obj.vendor, sender=user) | Q(receiver=user, sender=obj.vendor))
            return msg_obj.exists()
        return False

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'user_image']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'message_status', 'messages', 'is_read']

class SendMessageSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()
    message = serializers.CharField()

class StartMessagesSerializer(serializers.Serializer):
    product_name = serializers.CharField(required=False)


class CheckoutFormSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    username = serializers.EmailField()
    contact_number = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=50)
    zip_code = serializers.CharField(max_length=10)
    same_address = serializers.BooleanField(required=False)
    save_info = serializers.BooleanField(required=False)
    offer_discount = serializers.CharField(max_length=10, required=False)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)


# ================================== SERVICE PROVIDER ============================================
class ServiceProviderSerializer(serializers.ModelSerializer):
    provider = UserSerializer()
    class Meta:
        model = ServiceProviderDetails
        fields = '__all__'

class ServiceProviderProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProviderDetails
        fields = ['service_type', 'service_area', 'average_cost_per_hour', 'years_experience']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_type', 'name', 'description', 'price_per_hour']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class AuthServiceProviderDetailsSerializer(serializers.ModelSerializer):
    service_type = serializers.CharField()
    add_service_type = serializers.CharField(required=False)
    service_area = serializers.CharField()
    add_service_area = serializers.CharField(required=False)
    
    class Meta:
        model = ServiceProviderDetails
        fields = ['service_type', 'add_service_type', 'service_area', 'add_service_area', 'average_cost_per_hour', 'years_experience']
    
    def to_internal_value(self, data):
        # Convert comma-separated strings to lists
        data = super().to_internal_value(data)
        data['service_type'] = [item.strip() for item in data['service_type'].split(',')] if data.get('service_type') else []
        data['add_service_type'] = [item.strip() for item in data['add_service_type'].split(',')] if data.get('add_service_type') else []
        data['service_area'] = [item.strip() for item in data['service_area'].split(',')] if data.get('service_area') else []
        data['add_service_area'] = [item.strip() for item in data['add_service_area'].split(',')] if data.get('add_service_area') else []
        return data

    def create(self, validated_data):
        add_service_type = validated_data.pop('add_service_type', [])
        add_service_area = validated_data.pop('add_service_area', [])
        
        # Merge additional service types and areas with the existing ones
        service_type = validated_data['service_type'] + add_service_type
        service_area = validated_data['service_area'] + add_service_area
        
        validated_data['service_type'] = service_type
        validated_data['service_area'] = service_area
        
        return super().create(validated_data)
# ================================== VENDOR ============================================

class VendorSerializer(serializers.ModelSerializer):
    vendor = UserSerializer()
    class Meta:
        model = VendorDetails
        fields = '__all__'

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_status', 'payment_status', 'customer_details', 'more_info']

# ================================== Blog ============================================

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = '__all__'