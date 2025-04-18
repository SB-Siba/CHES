import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from multiselectfield import MultiSelectField
from .manager import MyAccountManager
from helpers import utils
from decimal import Decimal
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length = 255,null=True,blank=True)
    email = models.EmailField(null=True, blank = True,unique = True)
    password = models.TextField(null=True,blank=True)
    contact = models.CharField(max_length= 10, null=True, blank=True)
    address = models.CharField(max_length= 450 , null=True, blank=True)
    city = models.CharField(max_length=30,null=True,blank=True)
    pin_code = models.IntegerField(null=True,blank=True)
    quiz_score = models.IntegerField(default = 0,null= True, blank= True)

    user_image = models.ImageField(upload_to='userprofie/',null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

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

    token = models.CharField(max_length=100, null=True, blank=True)

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

    def generate_reset_password_token(self):
        token = str(uuid.uuid4())
        self.token = token
        self.save()
        return token

    def reset_password(self, token, new_password):
        if self.token == token:
            self.set_password(new_password)
            self.token = None  # Clear the token after password reset
            self.save()
            return True
        return False
    

class CategoryForProduces(models.Model):
    category_name = models.CharField(max_length = 250,null = True,blank = True)

class CategoryForServices(models.Model):
    service_category = models.CharField(max_length = 250,null = True,blank = True)
    image = models.ImageField(upload_to='service_categories/', null=True, blank=True) 

    def __str__(self):
        return self.service_category

class GaredenQuizModel(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank= True)
    questionANDanswer = models.JSONField(null= False, blank= False) 


class GardeningProfile(models.Model):

    GENDER_CHOICES = (
        ("Male","Male"),
        ("Female","Female"),
        ("Others","Others")
    )
    CASTE_CHOICES = (
        ("General","General"),
        ("Others","Others")
    )
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    user = models.ForeignKey(User, on_delete= models.CASCADE, null= True, blank= True)
    garden_area = models.BigIntegerField(default = 0,null= True, blank= True)
    number_of_plants = models.BigIntegerField(default = 0,null= True, blank= True)
    number_of_unique_plants = models.BigIntegerField(default = 0,null= True, blank= True)
    garden_image = models.ImageField(upload_to='garden/',null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES,null=True,blank=True)
    caste = models.CharField(max_length=20, choices=CASTE_CHOICES,null=True,blank=True)


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
    reply = models.TextField(null=True, blank= True)
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
        ('Litre', 'Litre'),
        ('Units', 'Units'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,null= True, blank= True)
    produce_category = models.ForeignKey(CategoryForProduces,on_delete=models.CASCADE,null= True, blank= True)
    product_name = models.CharField(max_length=250,blank=True,null=True)
    product_image = models.ImageField(upload_to='productforsell/',null=True, blank=True)
    product_quantity = models.FloatField(null=True,blank=True)
    SI_units = models.CharField(max_length=20, choices=SI_UNIT_CHOICES,null=True,blank=True)
    amount_in_green_points = models.PositiveIntegerField(null=True,blank=True)
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
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='vendor_details')
    business_name = models.CharField(max_length=255)
    business_address = models.CharField(max_length=255)
    business_description = models.TextField()
    business_license_number = models.CharField(max_length=50)
    business_category = models.CharField(max_length=20, null=True,blank=True)
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
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , unique=True)
    description = models.TextField()
    taxable_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='vendor_products/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    reason = models.TextField(null=True, blank=True)
    green_coins_required = models.PositiveIntegerField(default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    ratings = models.JSONField(default=list, null=True, blank=True)

    gst_rate = models.DecimalField(max_digits=5, decimal_places=2,default=Decimal('0.00'))
    sgst = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), editable=False)
    cgst = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), editable=False)


    def calculate_avg_rating(self):
        """
        Calculate the average rating from the JSONField 'ratings'.
        Ratings is expected to be a list of dictionaries with a 'rating' key.
        """
        if not isinstance(self.ratings, list) or len(self.ratings) == 0:
            # If ratings is not a list or is an empty list, return 0 as the average rating
            return 0

        total_rating = 0
        num_ratings = len(self.ratings)

        # Iterate over the ratings list and calculate total rating
        for rating_data in self.ratings:
            try:
                # Attempt to get the 'rating' key from each rating dictionary and convert it to a float
                rating = float(rating_data.get('rating', 0))
                total_rating += rating
            except (TypeError, ValueError):
                # In case of any invalid data, continue with the next rating
                continue

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

        # Calculate taxable price as discounted price minus GST rate
        if self.discount_price > 0 and self.gst_rate is not None:
            self.taxable_price = self.discount_price - (self.discount_price * (self.gst_rate / Decimal('100.00')))
        else:
            self.taxable_price = self.discount_price

        if self.gst_rate is not None:
            # Calculate SGST and CGST by dividing the GST rate by 2
            half_gst = self.gst_rate / 2
            self.sgst = round(half_gst, 2)
            self.cgst = round(half_gst, 2) 

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
    rating = models.FloatField(default=0.0,null=True,blank=True)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', null=True, blank=True)  

    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = utils.generate_unique_id(5)
        super().save(*args, **kwargs)

    
class ServiceProviderDetails(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.JSONField(null=True, blank=True)
    service_area = models.JSONField()
    years_experience = models.IntegerField()

    def __str__(self):
        return f"{self.provider.full_name} - {self.service_type}"

class Service(models.Model):
    basis = (
        ("Hourly","Hourly"),
        ("Daily","Daily"),
        ("Monthly","Monthly"),
        ("Yearly","Yearly"),
        ("Service-based","Service-based"),

    )
    provider = models.ForeignKey(User, on_delete=models.CASCADE)
    produce_category = models.ForeignKey(CategoryForProduces,on_delete=models.CASCADE,null= True, blank= True)
    description = models.TextField()
    service_image = models.ImageField(upload_to='service/',null=True, blank=True)
    basis = models.CharField(max_length=255, choices= basis, default="Hourly")
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    service_type = models.ForeignKey(CategoryForServices, on_delete=models.CASCADE,null= True, blank= True)
    sp_details = models.ForeignKey(ServiceProviderDetails,on_delete=models.CASCADE,null= True, blank= True)
    discount_percentage_for_greencoins = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)
    green_coins_required = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Calculate green_coins_required based on price_per_hour and discount_percentage_for_greencoins
        if self.discount_percentage_for_greencoins > 0 and self.price_per_hour > 0:
            discount_value = (self.discount_percentage_for_greencoins / Decimal('100.00')) * self.price_per_hour
            # Adjust the calculation as per your coin requirement logic
            self.green_coins_required = int(discount_value)
        else:
            self.green_coins_required = 0
        super().save(*args, **kwargs)

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



class MediaGallery(models.Model):
    media_image = models.ImageField(upload_to='service/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True, blank=True)  # Add index


class NewsActivity(models.Model):
    TYPE_CHOICES = [
        ('News', 'News'),
        ('Activity', 'Activity'),
    ]
    slug = models.SlugField(max_length=255, null=True, blank=True, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='News')
    title = models.CharField(max_length=255)
    date = models.DateField()
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    date_of_news_or_event = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.title)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class VendorQRcode(models.Model):
    CHOICES = [
        ('Select', 'Select'),
        ('Deselect', 'Deselect'),
    ]
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='qr_code', null=True, blank=True)
    qr_code = models.ImageField(upload_to='vendor_qr_codes/', null=True, blank=True)
    type = models.CharField(max_length=10, choices=CHOICES, default='Deselect')
    def __str__(self):
        return self.qr_code