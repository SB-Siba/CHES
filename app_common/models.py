from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password

from .manager import MyAccountManager
from helpers import utils
from django.utils import timezone


class AdminIncome(models.Model):
    amount = models.FloatField(default = 0.0)
    date = models.DateField(null= True, blank= True)
    

class TempUser(models.Model):
    # if the user sign up but not complted the verification
    # after user verification the data of this table will go to User Table

    email = models.EmailField(null=True,blank=True,unique=True)
    password = models.TextField(null=True,blank=True)
    contact = models.CharField(max_length= 10, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)




class User(AbstractBaseUser, PermissionsMixin):
    CITIES = (
        ("Bhubaneswar","Bhubaneswar"),
        ("Cuttack","Cuttack"),
        ("Brahmapur","Brahmapur"),
        ("Puri","Puri"),
        ("Balasore","Balasore"),
    )
    full_name = models.CharField(max_length = 255,null=True,blank=True)
    email = models.EmailField(null=True, blank = True,unique = True)
    password = models.TextField(null=True,blank=True)
    contact = models.CharField(max_length= 10, null=True, blank=True)
    address = models.JSONField(null=True, blank=True)
    city = models.CharField(max_length=20, choices=CITIES,null=True,blank=True)
    quiz_score = models.IntegerField(default = 0,null= True, blank= True)

    user_image = models.ImageField(upload_to='userprofie/',null=True, blank=True)

    is_approved = models.BooleanField(default=False)

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

    def get_rank(self):
        higher_or_equal_scores_count = User.objects.filter(coins__gte=self.coins).count()
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
    product_quantity = models.FloatField(default=0.0,null=True,blank=True)
    SI_units = models.CharField(max_length=20, choices=SI_UNIT_CHOICES,default="Kilogram")
    ammount_in_green_points = models.PositiveIntegerField(default=0,null=True,blank=True)
    buying_status = models.CharField(max_length=20, choices=BUYINGSTATUS,null=True,blank=True)
    quantity_buyer_want = models.PositiveIntegerField(default=1,null=True,blank=True)
    ammount_based_on_quantity_buyer_want = models.PositiveBigIntegerField(default=0,null=True,blank=True)
    payment_link = models.CharField(max_length=20, choices=PAYMENTLINK,default="NotAvailable")
    date_time = models.DateTimeField(auto_now_add=True)