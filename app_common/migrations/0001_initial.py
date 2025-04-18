# Generated by Django 5.1.1 on 2025-01-08 06:00

import ckeditor.fields
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryForProduces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryForServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_category', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='service_categories/')),
            ],
        ),
        migrations.CreateModel(
            name='MediaGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_image', models.ImageField(blank=True, null=True, upload_to='service/')),
            ],
        ),
        migrations.CreateModel(
            name='NewsActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('type', models.CharField(choices=[('News', 'News'), ('Event', 'Event')], default='News', max_length=10)),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('content', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog_images/')),
                ('date_of_news_or_event', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('password', models.TextField(blank=True, null=True)),
                ('contact', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.CharField(blank=True, max_length=450, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('pin_code', models.IntegerField(blank=True, null=True)),
                ('quiz_score', models.IntegerField(blank=True, default=0, null=True)),
                ('user_image', models.ImageField(blank=True, null=True, upload_to='userprofie/')),
                ('is_approved', models.BooleanField(default=False)),
                ('is_rtg', models.BooleanField(default=False)),
                ('is_vendor', models.BooleanField(default=False)),
                ('is_serviceprovider', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('wallet', models.FloatField(default=0.0)),
                ('coins', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('ratings', models.JSONField(blank=True, default=list, null=True)),
                ('total_income', models.FloatField(default=0.0)),
                ('total_invest', models.FloatField(default=0.0)),
                ('facebook_link', models.URLField(blank=True, max_length=2048, null=True)),
                ('instagram_link', models.URLField(blank=True, max_length=2048, null=True)),
                ('twitter_link', models.URLField(blank=True, max_length=2048, null=True)),
                ('youtube_link', models.URLField(blank=True, max_length=2048, null=True)),
                ('token', models.CharField(blank=True, max_length=100, null=True)),
                ('meta_data', models.JSONField(blank=True, default=dict, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('pending', 'pending'), ('confirmed', 'confirmed'), ('completed', 'completed'), ('declined', 'declined')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gardener', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GardeningProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('garden_area', models.BigIntegerField(blank=True, default=0, null=True)),
                ('number_of_plants', models.BigIntegerField(blank=True, default=0, null=True)),
                ('number_of_unique_plants', models.BigIntegerField(blank=True, default=0, null=True)),
                ('garden_image', models.ImageField(blank=True, null=True, upload_to='garden/')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=20, null=True)),
                ('caste', models.CharField(blank=True, choices=[('General', 'General'), ('Others', 'Others')], max_length=20, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GardeningProfileUpdateReject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gardening_profile_update_id', models.BigIntegerField(blank=True, null=True)),
                ('reason', models.CharField(blank=True, max_length=250, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GardeningProfileUpdateRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('garden_area', models.BigIntegerField(blank=True, default=0, null=True)),
                ('number_of_plants', models.BigIntegerField(blank=True, default=0, null=True)),
                ('number_of_unique_plants', models.BigIntegerField(blank=True, default=0, null=True)),
                ('garden_image', models.ImageField(blank=True, null=True, upload_to='garden/')),
                ('changes', models.TextField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GaredenQuizModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionANDanswer', models.JSONField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=255, null=True)),
                ('products', models.JSONField(blank=True, default=dict, null=True)),
                ('coupon', models.CharField(blank=True, max_length=255, null=True)),
                ('order_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_meta_data', models.JSONField(blank=True, default=dict, null=True)),
                ('order_status', models.CharField(choices=[('Placed', 'Placed'), ('Accepted', 'Accepted'), ('Cancel', 'Cancel'), ('On_Way', 'On_Way'), ('Refund', 'Refund'), ('Return', 'Return'), ('Delivered', 'Delivered')], default='Placed', max_length=255)),
                ('razorpay_payment_id', models.TextField(blank=True, null=True)),
                ('razorpay_order_id', models.TextField(blank=True, null=True)),
                ('razorpay_signature', models.TextField(blank=True, null=True)),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Refunded', 'Refunded')], default='Paid', max_length=255)),
                ('customer_details', models.JSONField(blank=True, default=dict, null=True)),
                ('more_info', models.TextField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('transaction_id', models.TextField(blank=True, null=True)),
                ('can_edit', models.BooleanField(default=True)),
                ('rating_given', models.BooleanField(blank=True, default=False, null=True)),
                ('rating', models.FloatField(blank=True, default=0.0, null=True)),
                ('payment_screenshot', models.ImageField(blank=True, null=True, upload_to='payment_screenshots/')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductFromVendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('taxable_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('discount_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('max_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='vendor_products/')),
                ('stock', models.IntegerField(default=0)),
                ('category', models.CharField(max_length=100)),
                ('reason', models.TextField(blank=True, null=True)),
                ('green_coins_required', models.PositiveIntegerField(default=0)),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=10.0, max_digits=5)),
                ('ratings', models.JSONField(blank=True, default=list, null=True)),
                ('gst_rate', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=5)),
                ('sgst', models.DecimalField(decimal_places=2, default=Decimal('0.00'), editable=False, max_digits=5)),
                ('cgst', models.DecimalField(decimal_places=2, default=Decimal('0.00'), editable=False, max_digits=5)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_common.booking')),
            ],
        ),
        migrations.CreateModel(
            name='SellProduce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=250, null=True)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='productforsell/')),
                ('product_quantity', models.FloatField(blank=True, null=True)),
                ('SI_units', models.CharField(blank=True, choices=[('Kilogram', 'Kilogram'), ('Gram', 'Gram'), ('Litre', 'Litre'), ('Units', 'Units')], max_length=20, null=True)),
                ('amount_in_green_points', models.PositiveIntegerField(blank=True, null=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.CharField(choices=[('approved', 'approved'), ('rejected', 'rejected'), ('pending', 'pending')], default='pending', max_length=10)),
                ('reason', models.TextField(blank=True, null=True)),
                ('validity_duration_days', models.PositiveIntegerField(blank=True, null=True)),
                ('validity_end_date', models.DateTimeField(blank=True, null=True)),
                ('produce_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_common.categoryforproduces')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProduceBuy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=250, null=True)),
                ('SI_units', models.CharField(choices=[('Kilogram', 'Kilogram'), ('Gram', 'Gram'), ('Liter', 'Liter')], default='Kilogram', max_length=20)),
                ('rating_given', models.BooleanField(blank=True, default=False, null=True)),
                ('buying_status', models.CharField(blank=True, choices=[('BuyInProgress', 'BuyInProgress'), ('PaymentDone', 'PaymentDone'), ('BuyCompleted', 'BuyCompleted'), ('BuyRejected', 'BuyRejected')], max_length=20, null=True)),
                ('quantity_buyer_want', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('ammount_based_on_quantity_buyer_want', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('payment_link', models.CharField(choices=[('Send', 'Send'), ('NotAvailable', 'NotAvailable')], default='NotAvailable', max_length=20)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buying_user', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selling_user', to=settings.AUTH_USER_MODEL)),
                ('sell_produce', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_common.sellproduce')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('service_image', models.ImageField(blank=True, null=True, upload_to='service/')),
                ('basis', models.CharField(choices=[('Hourly', 'Hourly'), ('Daily', 'Daily'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly'), ('Service-based', 'Service-based')], default='Hourly', max_length=255)),
                ('price_per_hour', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('discount_percentage_for_greencoins', models.DecimalField(decimal_places=2, default=10.0, max_digits=5)),
                ('green_coins_required', models.PositiveIntegerField(default=0)),
                ('produce_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_common.categoryforproduces')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_common.categoryforservices')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_common.service'),
        ),
        migrations.CreateModel(
            name='ServiceProviderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.JSONField(blank=True, null=True)),
                ('service_area', models.JSONField()),
                ('years_experience', models.IntegerField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='sp_details',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_common.serviceproviderdetails'),
        ),
        migrations.CreateModel(
            name='User_Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=250)),
                ('message', models.TextField()),
                ('reply', models.TextField(blank=True, null=True)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('is_solve', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_title', models.CharField(blank=True, default='No Title', max_length=250, null=True)),
                ('activity_content', models.TextField(blank=True, null=True)),
                ('activity_image', models.ImageField(blank=True, null=True, upload_to='activity/')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('likes', models.JSONField(blank=True, default=list, null=True)),
                ('comments', models.JSONField(blank=True, default=list, null=True)),
                ('is_accepted', models.CharField(choices=[('approved', 'approved'), ('rejected', 'rejected'), ('pending', 'pending')], default='pending', max_length=10)),
                ('reject_reason', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VendorDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=255)),
                ('business_address', models.CharField(max_length=255)),
                ('business_description', models.TextField()),
                ('business_license_number', models.CharField(max_length=50)),
                ('business_category', models.CharField(blank=True, max_length=20, null=True)),
                ('establishment_year', models.PositiveIntegerField()),
                ('website', models.URLField(blank=True)),
                ('established_by', models.CharField(blank=True, max_length=100)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VendorQRcode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='vendor_qr_codes/')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qr_code', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
