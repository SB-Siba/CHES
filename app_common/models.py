from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from multiselectfield import MultiSelectField
from .manager import MyAccountManager
from helpers import utils
from decimal import Decimal
from django.utils import timezone
 

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length = 255,null=True,blank=True)
    email = models.EmailField(null=True, blank = True,unique = True)
    password = models.TextField(null=True,blank=True)
    contact = models.CharField(max_length= 10, null=True, blank=True)
    address = models.JSONField(null=True, blank=True)
    city = models.CharField(max_length=30,null=True,blank=True)
    quiz_score = models.IntegerField(default = 0,null= True, blank= True)

    user_image = models.ImageField(upload_to='userprofie/',null=True, blank=True)

    is_approved = models.BooleanField(default=False)

    is_rtg = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_serviceprovider = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    wallet = models.FloatField(default=0.0)
    coins = models.PositiveBigIntegerField(default=0,null=True,blank=True)
    ratings = models.JSONField(default=list,null=True,blank=True)

    total_income = models.FloatField(default=0.0)
    total_invest = models.FloatField(default=0.0)

    facebook_link = models.URLField(null=True,blank=True, max_length=2048)
    instagram_link = models.URLField(null=True,blank=True, max_length=2048)
    twitter_link = models.URLField(null=True,blank=True, max_length=2048)
    youtube_link = models.URLField(null=True,blank=True, max_length=2048)

    # we are storing some extra data in the meta data field
    meta_data = models.JSONField(default= dict, null=True, blank = True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # def get_rank(self):
    #     higher_scores_count = User.objects.filter(coins__gt=self.coins).count()
    #     return higher_scores_count + 1

    def get_rank(self, user_type):
        if user_type == 'vendor':
            higher_or_equal_scores_count = User.objects.filter(
                is_vendor=True,
                coins__gte=self.coins
            ).count()
        elif user_type == 'serviceprovider':
            higher_or_equal_scores_count = User.objects.filter(
                is_serviceprovider=True,
                coins__gte=self.coins
            ).count()
        elif user_type == 'rtg':
            higher_or_equal_scores_count = User.objects.filter(
                is_rtg=True,
                coins__gte=self.coins
            ).count()
        else:
            higher_or_equal_scores_count = 0  # Handle invalid user type

        return higher_or_equal_scores_count

    def calculate_avg_rating(self):
        total_rating = 0
        num_ratings = len(self.ratings)

        # Calculate total rating
        for rating_data in self.ratings:
            rating = float(rating_data['rating'])  # Convert rating to float
            total_rating += rating

        # Calculate average rating
        if num_ratings > 0:
            avg_rating = total_rating / num_ratings
            avg_rating = round(avg_rating, 1)  # Round to 2 decimal places
        else:
            avg_rating = 0

        return avg_rating

class GaredenQuizModel(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank= True)
    questionANDanswer = models.JSONField(null= False, blank= False) 

class GardeningProfile(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank= True)
    garden_area = models.BigIntegerField(default = 0,null= True, blank= True)
    number_of_plants = models.BigIntegerField(default = 0,null= True, blank= True)
    number_of_unique_plants = models.BigIntegerField(default = 0,null= True, blank= True)
    garden_image = models.ImageField(upload_to='garden/',null=True, blank=True)


class GardeningProfileUpdateRequest(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank= True)
    garden_area = models.BigIntegerField(default = 0,null= True, blank= True)
    number_of_plants = models.BigIntegerField(default = 0,null= True, blank= True)
    number_of_unique_plants = models.BigIntegerField(default = 0,null= True, blank= True)
    garden_image = models.ImageField(upload_to='garden/',null=True, blank=True)
    changes = models.TextField(null= False, blank= False) 

class GardeningProfileUpdateReject(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank= True)
    gardening_profile_update_id = models.BigIntegerField(null=True,blank=True)
    reason = models.CharField(max_length = 250,null = True,blank = True)

class UserActivity(models.Model):
    ACCEPTREJECT = (
        ("approved","approved"),
        ("rejected","rejected"),
        ("pending","pending")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null= True, blank= True)
    activity_title = models.CharField(max_length=250,blank=True,null=True,default="No Title")
    activity_content = models.TextField(null=True,blank=True)
    activity_image = models.ImageField(upload_to='activity/',null=True, blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    likes = models.JSONField(default=list,null=True, blank=True)
    comments = models.JSONField(default=list,null=True, blank=True)
    is_accepted = models.CharField(max_length=10, choices= ACCEPTREJECT, default='pending')
    reject_reason = models.TextField(null=True, blank=True)



class User_Query(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    full_name = models.CharField(max_length=250,null=False, blank= False)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=250, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_solve = models.BooleanField(default = False)


class SellProduce(models.Model):
    APPROVEREJECT = (
        ("approved","approved"),
        ("rejected","rejected"),
        ("pending","pending")
    )
    SI_UNIT_CHOICES = [
        ('Kilogram', 'Kilogram'),
        ('Gram', 'Gram'),
        ('Liter', 'Liter'),
        ('Units', 'Units'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,null= True, blank= True)
    product_name = models.CharField(max_length=250,blank=True,null=True,default="No Title")
    product_image = models.ImageField(upload_to='productforsell/',null=True, blank=True)
    product_quantity = models.FloatField(default=0.0,null=True,blank=True)
    SI_units = models.CharField(max_length=20, choices=SI_UNIT_CHOICES,null=True,blank=True)
    ammount_in_green_points = models.PositiveIntegerField(default=0,null=True,blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    is_approved = models.CharField(max_length=10, choices= APPROVEREJECT, default='pending')
    reason = models.TextField(null=True, blank=True)
    validity_duration_days = models.PositiveIntegerField(null=True, blank=True)
    validity_end_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set validity end date based on current date and time
        if self.validity_duration_days is not None and self.validity_duration_days > 0:
            self.validity_end_date = timezone.now() + timezone.timedelta(days=self.validity_duration_days)
        else:
            # Set default validity duration as 7 days if not provided by seller
            self.validity_duration_days = 7
            self.validity_end_date = timezone.now() + timezone.timedelta(days=self.validity_duration_days)
        super().save(*args, **kwargs)

    def days_left_to_expire(self):
        if self.validity_end_date:
            delta = self.validity_end_date - timezone.now()
            remaining_days = max(0, delta.days)
            if remaining_days == 0 or  self.product_quantity == 0.0:
                self.delete()
            return remaining_days
        return 0

class ProduceBuy(models.Model):
    SI_UNIT_CHOICES = [
        ('Kilogram', 'Kilogram'),
        ('Gram', 'Gram'),
        ('Liter', 'Liter'),
    ]
    BUYINGSTATUS = [
        ('BuyInProgress', 'BuyInProgress'),
        ('PaymentDone', 'PaymentDone'),
        ('BuyCompleted', 'BuyCompleted'),
        ('BuyRejected', 'BuyRejected'),
    ]
    PAYMENTLINK = [
        ('Send', 'Send'),
        ('NotAvailable', 'NotAvailable'),
    ]
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name='selling_user',null=True,blank=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE , related_name='buying_user',null=True,blank=False)
    # sell_produce = models.CharField(max_length=250, blank=True, null=True)
    sell_produce = models.ForeignKey(SellProduce,on_delete=models.SET_NULL, blank=True, null=True)
    product_name = models.CharField(max_length=250, blank=True, null=True)
    # product_quantity = models.FloatField(default=0.0,null=True,blank=True)
    SI_units = models.CharField(max_length=20, choices=SI_UNIT_CHOICES,default="Kilogram")
    rating_given = models.BooleanField(default=False,null=True,blank=True)
    buying_status = models.CharField(max_length=20, choices=BUYINGSTATUS,null=True,blank=True)
    quantity_buyer_want = models.PositiveIntegerField(default=1,null=True,blank=True)
    ammount_based_on_quantity_buyer_want = models.PositiveBigIntegerField(default=0,null=True,blank=True)
    payment_link = models.CharField(max_length=20, choices=PAYMENTLINK,default="NotAvailable")
    date_time = models.DateTimeField(auto_now_add=True)

class VendorDetails(models.Model):
    BUSINESS_CATEGORIES = (
        ('plants', 'Plants'),
        ('tools', 'Tools'),
        ('seeds', 'Seeds'),
        ('other', 'Other'),
    )
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='vendor_details')
    business_name = models.CharField(max_length=255)
    business_address = models.CharField(max_length=255)
    business_description = models.TextField()
    business_license_number = models.CharField(max_length=50)
    business_category = models.CharField(max_length=20, choices=BUSINESS_CATEGORIES)
    establishment_year = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    established_by = models.CharField(max_length=100, blank=True)

    def __str__(self):
        if self.vendor:
            return f"{self.business_name} - {self.vendor.full_name}"
        return self.business_name
    
    def get_vendor_rating(self):
        if self.vendor:
            return self.vendor.calculate_avg_rating()
        return 0
    

class ProductFromVendor(models.Model):
    CATEGORY_CHOICES = [
        ('seeds', 'Seeds'),
        ('plants', 'Plants'),
        ('tools', 'Gardening Tools'),
        ('fertilizers', 'Fertilizers'),
        ('pots_containers', 'Pots & Containers'),
        ('pest_control', 'Pest Control'),
        ('irrigation', 'Irrigation Systems'),
        ('garden_decor', 'Garden Decor'),
        # Add more gardening-specific categories as needed
    ]
    
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='vendor_products/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    reason = models.TextField(null=True, blank=True)
    green_coins_required = models.PositiveIntegerField(default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    ratings = models.JSONField(default=list, null=True, blank=True)

    def calculate_discounted_price(self):
        """
        Calculate the discounted price based on the discount percentage.
        """
        if self.discount_percentage > 0:
            discount_amount = (self.discount_percentage / 100) * self.discount_price
            discounted_price = self.discount_price - discount_amount
            return discounted_price
        else:
            return self.discount_price
    
    def calculate_avg_rating(self):
        total_rating = 0
        num_ratings = len(self.ratings)

        # Calculate total rating
        for rating_data in self.ratings:
            rating = float(rating_data['rating'])  # Convert rating to float
            total_rating += rating

        # Calculate average rating
        if num_ratings > 0:
            avg_rating = total_rating / num_ratings
            avg_rating = round(avg_rating, 1)  # Round to 1 decimal place
        else:
            avg_rating = 0

        return avg_rating

    def save(self, *args, **kwargs):
        # Calculate green_coins_required as a percentage of the discount_price
        if self.discount_price > 0 and self.discount_percentage > 0:
            self.green_coins_required = int((self.discount_percentage / Decimal('100.00')) * self.discount_price)
        else:
            self.green_coins_required = 0
        super(ProductFromVendor, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} --> {self.vendor.full_name}"
    
class Order(models.Model):
    ORDER_STATUS = (
        ("Placed","Placed"),
        ("Accepted","Accepted"),
        ("Cancel","Cancel"),
        ("On_Way","On_Way"),
        ("Refund","Refund"),
        ("Return","Return"),
        ("Delivered","Delivered"),
    )

    PaymentStatus = (
        ("Paid","Paid"),
        ("Pending","Pending"),
        ("Refunded","Refunded"),
    )

    uid=models.CharField(max_length=255, null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="customer")
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="vendor")
    products = models.JSONField(default=dict, null=True, blank=True)
    coupon = models.CharField(max_length=255, null=True, blank=True)
    order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_meta_data = models.JSONField(default=dict, null=True, blank=True)
    order_status = models.CharField(max_length=255, choices= ORDER_STATUS, default="Placed")
    razorpay_payment_id = models.TextField(null= True, blank=True)
    razorpay_order_id = models.TextField(null= True, blank=True)
    razorpay_signature = models.TextField(null= True, blank=True)
    payment_status = models.CharField(max_length=255, choices= PaymentStatus, default="Paid")

    customer_details = models.JSONField(default=dict, null=True, blank=True)

    more_info = models.TextField(null= True, blank=True)
    date = models.DateField(auto_now_add= True, null=True, blank=True)

    transaction_id = models.TextField(null= True, blank=True)
    can_edit = models.BooleanField(default=True) # id a order is canceled or refunded, make it non editable
    rating_given = models.BooleanField(default=False,null=True,blank=True)
    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.generate_unique_id(5)
        super().save(*args, **kwargs)

class ServiceProviderDetails(models.Model):
    SERVICE_TYPES = [
        ('Lawn Care', 'Lawn Care'),
        ('Tree Trimming', 'Tree Trimming'),
        ('Garden Design', 'Garden Design'),
        ('Irrigation Systems', 'Irrigation Systems'),
        # Add more types as needed
    ]
    SERVICE_AREAS = (
        ("Bhubaneswar","Bhubaneswar"),
        ("Cuttack","Cuttack"),
        ("Brahmapur","Brahmapur"),
        ("Puri","Puri"),
        ("Balasore","Balasore"),
    )
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.TextField()
    service_area = models.TextField()
    average_cost_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    years_experience = models.IntegerField()

    def __str__(self):
        return f"{self.provider.full_name} - {self.service_type}"

class Service(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    service_type = models.CharField(max_length=100, blank=True)

class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    gardener = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=(('pending', 'pending'), ('confirmed', 'confirmed'), ('completed', 'completed'), ('declined', 'declined')), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
