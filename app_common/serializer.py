from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import (
    Booking,
    CategoryForProduces,
    Order,
    ProduceBuy,
    ProductFromVendor,
    SellProduce,
    Service,
    User, 
    GardeningProfile, 
    GaredenQuizModel,
    User_Query, 
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
    # Assuming custom_business_category will be an optional field
    custom_business_category = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = VendorDetails
        fields = [
            'business_name',
            'business_address',
            'business_description',
            'business_license_number',
            'business_category',
            'custom_business_category',  # Add this field to handle custom category input
            'establishment_year',
            'website',
            'established_by'
        ]

    def validate(self, data):
        # Example validation to ensure custom business category is provided if 'other' is selected
        if data.get('business_category') == 'other' and not data.get('custom_business_category'):
            raise serializers.ValidationError({
                'custom_business_category': 'This field is required if "business_category" is set to "other".'
            })
        return data

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
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = SellProduce
        fields = '__all__'  # All fields including the new field

    def get_user_full_name(self, obj):
        # Ensure that the user exists and return the full name
        if obj.user:
            return obj.user.get_full_name() if hasattr(obj.user, 'get_full_name') else f"{obj.user.full_name}"
        return None

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
    user_full_name = serializers.SerializerMethodField()
    class Meta:
        model = UserActivity
        fields = ['id','user_full_name', 'is_accepted', 'likes', 'comments', 'like_count', 'comment_count', 'user_liked','activity_image','activity_title','activity_content']

    def get_like_count(self, obj):
        return len(obj.likes)

    def get_comment_count(self, obj):
        return len(obj.comments)

    def get_user_liked(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            return request.user.full_name in obj.likes
        return False
    
    def get_user_full_name(self,obj):
        return obj.user.full_name


class CommentSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    comment = serializers.CharField(max_length=1000)

class RateOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
    rating = serializers.FloatField(required=True, min_value=0, max_value=5)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'user_image']


class ProductFromVendorSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(source='calculate_avg_rating', read_only=True)
    discounted_price = serializers.DecimalField(source='calculate_discounted_price', max_digits=10, decimal_places=2, read_only=True)
    has_message = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()  # Use method field for vendor
    
    class Meta:
        model = ProductFromVendor
        fields = [
            'id', 'vendor', 'name', 'description', 'discount_price', 'max_price',
            'image', 'stock', 'category', 'reason', 'green_coins_required',
            'discount_percentage', 'ratings', 'average_rating', 'discounted_price', 'has_message'
        ]

    def get_vendor(self, obj):
        # Manually serialize the vendor object using the UserSerializer
        return UserSerializer(obj.vendor, context=self.context).data

    def get_has_message(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            msg_obj = Message.objects.filter(Q(receiver=obj.vendor, sender=user) | Q(receiver=user, sender=obj.vendor))
            return msg_obj.exists()
        return False



class ServiceDetailsSerializer(serializers.ModelSerializer):
    provider = UserSerializer()
    class Meta:
        model = Service
        fields = ['id','provider','service_type', 'name', 'description', 'price_per_hour']
        
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()
    class Meta:
        model = Message
        fields = ['id','sender', 'receiver','message_status', 'messages', 'is_read','last_message']

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
        fields = ['average_cost_per_hour', 'years_experience']  # Exclude service_type and service_area

    def update(self, instance, validated_data):
        # Update average_cost_per_hour and years_experience
        instance.average_cost_per_hour = validated_data.get('average_cost_per_hour', instance.average_cost_per_hour)
        instance.years_experience = validated_data.get('years_experience', instance.years_experience)
        
        # Save the instance
        instance.save()
        return instance

class ServiceSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.full_name', read_only=True)
    provider_id = serializers.IntegerField(source='provider.id', read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'service_type', 'name', 'description', 'price_per_hour', 'provider_id', 'provider_name']

class BookingSerializer(serializers.ModelSerializer):
    gardener_full_name = serializers.SerializerMethodField()
    provider_full_name = serializers.SerializerMethodField()
    provider_id = serializers.SerializerMethodField()
    service_name = serializers.SerializerMethodField()  # Add service name field
    service_price_per_hour = serializers.SerializerMethodField()  # Add service price per hour field
    created_at = serializers.DateTimeField(format='%Y-%m-%d at %H:%M')
    booking_date = serializers.DateTimeField(format='%Y-%m-%d at %H:%M')

    class Meta:
        model = Booking
        fields = '__all__'
        extra_fields = [
            'gardener_full_name', 'provider_full_name', 'provider_id',
            'service_name', 'service_price_per_hour'
        ]

    def get_gardener_full_name(self, obj):
        if obj.gardener:
            return obj.gardener.full_name if obj.gardener.full_name else None
        return None

    def get_provider_full_name(self, obj):
        if obj.service and obj.service.provider:
            return obj.service.provider.full_name if obj.service.provider.full_name else None
        return None

    def get_provider_id(self, obj):
        if obj.service and obj.service.provider:
            return obj.service.provider.id
        return None

    def get_service_name(self, obj):
        if obj.service:
            return obj.service.name
        return None

    def get_service_price_per_hour(self, obj):
        if obj.service:
            return obj.service.price_per_hour
        return None



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
    blog_by = serializers.SerializerMethodField()

    class Meta:
        model = Blogs
        fields = ['id','slug','title', 'author', 'date', 'content', 'image', 'blog_by']

    def get_blog_by(self,obj):
        if obj.user.full_name:
            return obj.user.full_name
        else:
            return obj.user.email
# Rank Serializer

class UserRankSerializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()
    is_rtg = serializers.BooleanField()  # To show if the user is RTG
    is_vendor = serializers.BooleanField()  # To show if the user is Vendor
    user_image = serializers.ImageField()  # To show the user's profile image

    class Meta:
        model = User
        fields = ['full_name', 'email', 'coins', 'rank', 'is_rtg', 'is_vendor', 'user_image']  # Add more fields if needed

    def get_rank(self, obj):
        # Calculate the rank based on the number of users with more coins
        higher_scores_count = User.objects.filter(coins__gt=obj.coins).count()
        return higher_scores_count + 1


class CategoryForProducesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryForProduces
        fields = ['id', 'category_name']


class UserQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Query
        fields = ['id', 'user', 'full_name', 'email', 'subject', 'message', 'date_sent', 'is_solve']
        read_only_fields = ['id', 'date_sent']