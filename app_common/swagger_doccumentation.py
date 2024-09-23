from drf_yasg import openapi

signup_post = [
    openapi.Parameter("full_name", openapi.IN_QUERY, description="Full Name", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("email", openapi.IN_QUERY, description="Email", required=True, format=openapi.FORMAT_EMAIL, type=openapi.TYPE_STRING),
    openapi.Parameter("password", openapi.IN_QUERY, description="Password", format=openapi.FORMAT_PASSWORD, required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("confirm_password", openapi.IN_QUERY, description="Confirm Password", format=openapi.FORMAT_PASSWORD, required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("contact", openapi.IN_QUERY, description="Contact", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("city", openapi.IN_QUERY, description="City", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("is_rtg", openapi.IN_QUERY, description="Is RTG", required=False, type=openapi.TYPE_BOOLEAN),
    openapi.Parameter("is_vendor", openapi.IN_QUERY, description="Is Vendor", required=False, type=openapi.TYPE_BOOLEAN),
    openapi.Parameter("is_serviceprovider", openapi.IN_QUERY, description="Is Service Provider", required=False, type=openapi.TYPE_BOOLEAN),
]

login_post = [
    openapi.Parameter("username", openapi.IN_QUERY, description="Email", required=True, format=openapi.FORMAT_EMAIL, type=openapi.TYPE_STRING),
    openapi.Parameter("password", openapi.IN_QUERY, description="Password", format=openapi.FORMAT_PASSWORD, required=True, type=openapi.TYPE_STRING),
]

gardening_details_post = [
    openapi.Parameter("garden_area", openapi.IN_QUERY, description="Garden Area", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("number_of_plants", openapi.IN_QUERY, description="Number of Plants", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("number_of_unique_plants", openapi.IN_QUERY, description="Number of Unique Plants", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("garden_image", openapi.IN_QUERY, description="Garden Image", required=True, type=openapi.TYPE_FILE),
]

gardening_quiz_post = [
    openapi.Parameter("q1", openapi.IN_QUERY, description="1. What is the process of cutting off dead or overgrown branches called?", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("q2", openapi.IN_QUERY, description="2. Which of the following is a perennial flower?", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("q3", openapi.IN_QUERY, description="3. What is the best time of day to water plants?", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("q4", openapi.IN_QUERY, description="4. Which type of soil holds water the best?", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("q5", openapi.IN_QUERY, description="5. What is the primary purpose of adding compost to soil?", required=True, type=openapi.TYPE_STRING),
]

gardening_quiz_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

logout_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

vendor_details_post = [
    openapi.Parameter("business_name", openapi.IN_QUERY, description="Business Name", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("business_address", openapi.IN_QUERY, description="Business Address", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("business_description", openapi.IN_QUERY, description="Business Description", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("business_license_number", openapi.IN_QUERY, description="Business License Number", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("business_category", openapi.IN_QUERY, description="Business Category", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("establishment_year", openapi.IN_QUERY, description="Establishment Year", required=True, type=openapi.TYPE_INTEGER),
    openapi.Parameter("website", openapi.IN_QUERY, description="Website", required=False, type=openapi.TYPE_STRING),
    openapi.Parameter("established_by", openapi.IN_QUERY, description="Established By", required=True, type=openapi.TYPE_STRING),
]

service_provider_details_post = [
    openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="Bearer token for authentication",
        type=openapi.TYPE_STRING,
        required=True
    ),
    openapi.Parameter(
        'service_type',
        openapi.IN_FORM,
        description="Comma-separated list of service types. Example: Lawn Care, Garden Design",
        type=openapi.TYPE_STRING,
        required=True
    ),
    openapi.Parameter(
        'add_service_type',
        openapi.IN_FORM,
        description="Comma-separated list of additional service types. Example: Pest Control, Landscaping",
        type=openapi.TYPE_STRING,
        required=False
    ),
    openapi.Parameter(
        'service_area',
        openapi.IN_FORM,
        description="Comma-separated list of service areas. Example: Bhubaneswar, Cuttack",
        type=openapi.TYPE_STRING,
        required=True
    ),
    openapi.Parameter(
        'add_service_area',
        openapi.IN_FORM,
        description="Comma-separated list of additional service areas. Example: Kolkata, Puri",
        type=openapi.TYPE_STRING,
        required=False
    ),
    openapi.Parameter(
        'average_cost_per_hour',
        openapi.IN_FORM,
        description="Average cost per hour for the services. Example: 25.50",
        type=openapi.TYPE_NUMBER,
        required=True
    ),
    openapi.Parameter(
        'years_experience',
        openapi.IN_FORM,
        description="Number of years of experience. Example: 5",
        type=openapi.TYPE_INTEGER,
        required=True
    )
] 

user_profile_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

update_profile_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

update_profile_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('full_name', openapi.IN_FORM, description="Full name of the user", type=openapi.TYPE_STRING),
    openapi.Parameter('email', openapi.IN_FORM, description="Email address of the user", type=openapi.TYPE_STRING),
    openapi.Parameter('contact', openapi.IN_FORM, description="Contact number of the user", type=openapi.TYPE_STRING),
    openapi.Parameter('facebook_link', openapi.IN_FORM, description="Facebook profile link of the user", type=openapi.TYPE_STRING),
    openapi.Parameter('instagram_link', openapi.IN_FORM, description="Instagram profile link of the user", type=openapi.TYPE_STRING),
    openapi.Parameter('twitter_link', openapi.IN_FORM, description="Twitter profile link of the user", type=openapi.TYPE_STRING),
    openapi.Parameter('youtube_link', openapi.IN_FORM, description="YouTube profile link of the user", type=openapi.TYPE_STRING),
    openapi.Parameter('address', openapi.IN_FORM, description="Address of the user", type=openapi.TYPE_STRING),
    openapi.Parameter('user_image', openapi.IN_FORM, description="Base64 encoded image data of the user's profile picture", type=openapi.TYPE_STRING),
    openapi.Parameter('password', openapi.IN_FORM, description="New password for the user", type=openapi.TYPE_STRING),
]

update_gardening_profile_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('garden_area', openapi.IN_FORM, description="Garden area", type=openapi.TYPE_INTEGER),
    openapi.Parameter('number_of_plants', openapi.IN_FORM, description="Number of plants", type=openapi.TYPE_INTEGER),
    openapi.Parameter('number_of_unique_plants', openapi.IN_FORM, description="Number of unique plants", type=openapi.TYPE_INTEGER),
    openapi.Parameter('garden_image', openapi.IN_FORM, description="Base64 encoded image data of the garden", type=openapi.TYPE_STRING),
]

add_activity_request_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('activity_title', openapi.IN_FORM, description="Title of the activity", type=openapi.TYPE_STRING),
    openapi.Parameter('activity_content', openapi.IN_FORM, description="Content of the activity", type=openapi.TYPE_STRING),
    openapi.Parameter('activity_image', openapi.IN_FORM, description="Image for the activity", type=openapi.TYPE_FILE),
]

activity_list_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

sell_produce_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('produce_category', openapi.IN_FORM, description="ID of the produce category", type=openapi.TYPE_INTEGER),  # New field
    openapi.Parameter('product_name', openapi.IN_FORM, description="Name of the product", type=openapi.TYPE_STRING),
    openapi.Parameter('product_image', openapi.IN_FORM, description="Image of the product", type=openapi.TYPE_FILE),
    openapi.Parameter('product_quantity', openapi.IN_FORM, description="Quantity of the product", type=openapi.TYPE_NUMBER),
    openapi.Parameter('SI_units', openapi.IN_FORM, description="Units of the product quantity", type=openapi.TYPE_STRING),
    openapi.Parameter('ammount_in_green_points', openapi.IN_FORM, description="Amount in green points", type=openapi.TYPE_INTEGER),
    openapi.Parameter('validity_duration_days', openapi.IN_FORM, description="Validity duration in days", type=openapi.TYPE_INTEGER),
]

sell_produces_list_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

green_commerce_product_community_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

buying_begins_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('quantity', openapi.IN_FORM, description="Quantity the buyer wants to purchase", type=openapi.TYPE_INTEGER),
]

buy_begins_seller_view_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

buy_begins_buyer_view_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

send_payment_link_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("ammount_based_on_buyer_quantity", openapi.IN_FORM, description="Amount based on buyer quantity", required=True, type=openapi.TYPE_INTEGER),
]

reject_buy_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

produce_buy_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

all_orders_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

all_posts_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

plus_like_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("activity_id", openapi.IN_QUERY, description="ID of the activity to like", required=True, type=openapi.TYPE_INTEGER),
]

minus_like_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("activity_id", openapi.IN_QUERY, description="ID of the activity to unlike", required=True, type=openapi.TYPE_INTEGER),
]

add_comment_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("post", openapi.IN_FORM, description="ID of the post to comment on", required=True, type=openapi.TYPE_INTEGER),
    openapi.Parameter("comment", openapi.IN_FORM, description="Comment content", required=True, type=openapi.TYPE_STRING),
]

delete_comment_delete = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("post_id", openapi.IN_PATH, description="ID of the post", required=True, type=openapi.TYPE_INTEGER),
    openapi.Parameter("comment_id", openapi.IN_PATH, description="ID of the comment to delete", required=True, type=openapi.TYPE_STRING),
]

get_all_comments_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("post_id", openapi.IN_QUERY, description="ID of the post to get comments for", required=True, type=openapi.TYPE_INTEGER),
]

rate_order_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("order_id", openapi.IN_FORM, description="ID of the order to be rated", required=True, type=openapi.TYPE_INTEGER),
    openapi.Parameter("rating", openapi.IN_FORM, description="Rating for the order (0-5, including decimals)", required=True, type=openapi.TYPE_NUMBER, format='float'),
]

vendor_products_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

fetch_user_details_get = [
    openapi.Parameter("user_id", openapi.IN_QUERY, description="ID of the user", required=True, type=openapi.TYPE_INTEGER),
]

start_message_post = [
    openapi.Parameter("r_id", openapi.IN_PATH, description="ID of the receiver", required=True, type=openapi.TYPE_INTEGER),
    openapi.Parameter("product_name", openapi.IN_FORM, description="Name of the product (optional)", required=False, type=openapi.TYPE_STRING),
]

send_message_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("receiver_id", openapi.IN_FORM, description="ID of the receiver", required=True, type=openapi.TYPE_INTEGER),
    openapi.Parameter("message", openapi.IN_FORM, description="Message to be sent", required=True, type=openapi.TYPE_STRING),
]

fetch_messages_get = [
    openapi.Parameter("receiver_id", openapi.IN_QUERY, description="ID of the receiver", required=True, type=openapi.TYPE_INTEGER),
]

service_provider_list_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

checkout_get = [
    openapi.Parameter("offer_discount", openapi.IN_QUERY, description="Offer discount", type=openapi.TYPE_STRING),
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", type=openapi.TYPE_STRING, required=True),
]

checkout_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("offer_discount", openapi.IN_FORM, description="Offer discount", type=openapi.TYPE_STRING, required=False),
    openapi.Parameter("first_name", openapi.IN_FORM, description="First Name", type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("last_name", openapi.IN_FORM, description="Last Name", type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("username", openapi.IN_FORM, description="Username", type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("contact_number", openapi.IN_FORM, description="Contact Number", type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("email", openapi.IN_FORM, description="Email", type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("address", openapi.IN_FORM, description="Address", type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("city", openapi.IN_FORM, description="City", type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("zip_code", openapi.IN_FORM, description="Zip Code", type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("same_address", openapi.IN_FORM, description="Same Address", type=openapi.TYPE_BOOLEAN, required=False),
    openapi.Parameter("save_info", openapi.IN_FORM, description="Save Info", type=openapi.TYPE_BOOLEAN, required=False),
]

orders_from_vendors_parameters = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", type=openapi.TYPE_STRING, required=True),
]

forgot_password = [
    openapi.Parameter("email", openapi.IN_FORM, description="User Email", type=openapi.TYPE_STRING, required=True),
]

reset_password = [
    openapi.Parameter("password", openapi.IN_FORM, description="Password", type=openapi.TYPE_STRING, required=True),
    openapi.Parameter("confirm_password", openapi.IN_FORM, description="Confirm Password", type=openapi.TYPE_STRING, required=True),
]

# ------------------------------------ Service Provider ----------------------------------
service_provider_profile_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

service_provider_update_profile_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('service_type', openapi.IN_FORM, description="Service types provided by the service provider (comma-separated)", type=openapi.TYPE_STRING),
    openapi.Parameter('service_area', openapi.IN_FORM, description="Service areas covered by the service provider (comma-separated)", type=openapi.TYPE_STRING),
    openapi.Parameter('average_cost_per_hour', openapi.IN_FORM, description="Average cost per hour charged by the service provider", type=openapi.TYPE_NUMBER),
    openapi.Parameter('years_experience', openapi.IN_FORM, description="Years of experience of the service provider", type=openapi.TYPE_INTEGER),
    openapi.Parameter('image', openapi.IN_FORM, description="Image file of the service provider", type=openapi.TYPE_FILE),
]

service_list_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

service_list_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('service_type', openapi.IN_FORM, description="Type of service", type=openapi.TYPE_STRING),
    openapi.Parameter('name', openapi.IN_FORM, description="Name of the service", type=openapi.TYPE_STRING),
    openapi.Parameter('description', openapi.IN_FORM, description="Description of the service", type=openapi.TYPE_STRING),
    openapi.Parameter('price_per_hour', openapi.IN_FORM, description="Price per hour for the service", type=openapi.TYPE_NUMBER),
]

service_update_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('service_id', openapi.IN_PATH, description="ID of the service to retrieve", type=openapi.TYPE_INTEGER),
]

service_update_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('service_id', openapi.IN_PATH, description="ID of the service to update", type=openapi.TYPE_INTEGER),
    openapi.Parameter('name', openapi.IN_FORM, description="Name of the service", type=openapi.TYPE_STRING),
    openapi.Parameter('description', openapi.IN_FORM, description="Description of the service", type=openapi.TYPE_STRING),
    openapi.Parameter('price_per_hour', openapi.IN_FORM, description="Price per hour for the service", type=openapi.TYPE_NUMBER),
]


service_delete_params = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('service_id', openapi.IN_PATH, description="ID of the service to delete", type=openapi.TYPE_INTEGER),
]

my_service_bookings_params = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

booking_action_params = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('booking_id', openapi.IN_PATH, description="ID of the booking", type=openapi.TYPE_INTEGER),
    openapi.Parameter('action', openapi.IN_PATH, description="Action to perform (confirm, decline, complete)", type=openapi.TYPE_STRING),
]

# ------------------------------------ Vendor ----------------------------------

vendor_profile_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

vendor_update_profile_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),

    openapi.Parameter(
        'business_name', openapi.IN_FORM, description="Business Name", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'business_address', openapi.IN_FORM, description="Business Address", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'business_description', openapi.IN_FORM, description="Business Description", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'business_license_number', openapi.IN_FORM, description="Business License Number", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'business_category', openapi.IN_FORM, description="Business Category", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'establishment_year', openapi.IN_FORM, description="Establishment Year", type=openapi.TYPE_INTEGER, required=True
    ),
    openapi.Parameter(
        'website', openapi.IN_FORM, description="Website", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'established_by', openapi.IN_FORM, description="Established By", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'image', openapi.IN_FORM, description="Profile Image", type=openapi.TYPE_FILE, required=False
    ),
]

vendor_sell_product_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),

    openapi.Parameter(
        'product_name', openapi.IN_FORM, description="Product Name", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'product_description', openapi.IN_FORM, description="Product Description", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'product_image', openapi.IN_FORM, description="Product Image", type=openapi.TYPE_FILE, required=True
    ),
    openapi.Parameter(
        'product_price', openapi.IN_FORM, description="Product Price", type=openapi.TYPE_NUMBER, required=True
    ),
    openapi.Parameter(
        'product_category', openapi.IN_FORM, description="Product Category", type=openapi.TYPE_STRING, required=True
    ),
]

vendor_sold_product_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]

sell_product_list_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
]
update_product_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),

    openapi.Parameter(
        'product_id', openapi.IN_PATH, description="ID of the product to update", type=openapi.TYPE_INTEGER
    ),
    openapi.Parameter(
        'name', openapi.IN_FORM, description="Product Name", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'description', openapi.IN_FORM, description="Product Description", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'discount_price', openapi.IN_FORM, description="Discount Price", type=openapi.TYPE_NUMBER, required=True
    ),
    openapi.Parameter(
        'max_price', openapi.IN_FORM, description="Maximum Price", type=openapi.TYPE_NUMBER, required=True
    ),
    openapi.Parameter(
        'image', openapi.IN_FORM, description="Product Image", type=openapi.TYPE_FILE, required=False
    ),
    openapi.Parameter(
        'stock', openapi.IN_FORM, description="Product Stock", type=openapi.TYPE_INTEGER, required=True
    ),
    openapi.Parameter(
        'category', openapi.IN_FORM, description="Product Category", type=openapi.TYPE_STRING, required=True
    ),
    openapi.Parameter(
        'reason', openapi.IN_FORM, description="Reason", type=openapi.TYPE_STRING, required=False
    ),
    openapi.Parameter(
        'green_coins_required', openapi.IN_FORM, description="Green Coins Required", type=openapi.TYPE_INTEGER, required=True
    ),
    openapi.Parameter(
        'discount_percentage', openapi.IN_FORM, description="Discount Percentage", type=openapi.TYPE_NUMBER, required=True
    )
]

delete_product_delete = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter('product_id', openapi.IN_PATH, description="ID of the product to delete", type=openapi.TYPE_INTEGER),
]

vendor_order_detail_get = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("order_uid", openapi.IN_PATH, description="UID of the order", required=True, type=openapi.TYPE_STRING),
]

vendor_order_detail_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("order_uid", openapi.IN_PATH, description="UID of the order", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("order_status", openapi.IN_FORM, description="Status of the order", required=False, type=openapi.TYPE_STRING, enum=["Placed", "Accepted", "Cancel", "On_Way", "Refund", "Return", "Delivered"]),
    openapi.Parameter("payment_status", openapi.IN_FORM, description="Payment status of the order", required=False, type=openapi.TYPE_STRING, enum=["Paid", "Pending", "Refunded"]),
    openapi.Parameter("customer_details", openapi.IN_FORM, description="Customer details in JSON format", required=False, type=openapi.TYPE_STRING),
    openapi.Parameter("more_info", openapi.IN_FORM, description="Additional information about the order", required=False, type=openapi.TYPE_STRING),
]



# Blog

blog_post_params = [
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer <token>",
            required=True,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'title',
            openapi.IN_FORM,
            description="Title of the blog",
            required=True,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'author',
            openapi.IN_FORM,
            description="Name of the author",
            required=True,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'date',
            openapi.IN_FORM,
            description="Date in YYYY-MM-DD format",
            required=True,
            type=openapi.TYPE_STRING,
            format='date'
        ),
        openapi.Parameter(
            'content',
            openapi.IN_FORM,
            description="Content of the blog (Rich Text)",
            required=True,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'image',
            openapi.IN_FORM,
            description="Image file for the blog",
            required=False,
            type=openapi.TYPE_FILE
        ),
    ]


blog_update_params = [
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description="Bearer <token>",
            required=True,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'blog_id',
            openapi.IN_PATH,
            description="ID of the blog to update",
            required=True,
            type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter(
            'title',
            openapi.IN_FORM,
            description="Title of the blog",
            required=False,  # It's an update, so not always required
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'author',
            openapi.IN_FORM,
            description="Name of the author",
            required=False,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'date',
            openapi.IN_FORM,
            description="Date in YYYY-MM-DD format",
            required=False,
            type=openapi.TYPE_STRING,
            format='date'
        ),
        openapi.Parameter(
            'content',
            openapi.IN_FORM,
            description="Content of the blog (Rich Text)",
            required=False,
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'image',
            openapi.IN_FORM,
            description="Image file for the blog",
            required=False,
            type=openapi.TYPE_FILE
        )
    ]


list_services_params = [
    openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="Bearer <token>",
        required=True,
        type=openapi.TYPE_STRING
    ),
]

service_search_params = [
    openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="Bearer <token>",
        required=True,
        type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        'search_query',
        openapi.IN_QUERY,
        description="Search services by name or type",
        required=False,
        type=openapi.TYPE_STRING
    ),
]



my_booked_services_params = [
    openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="Bearer <token>",
        required=True,
        type=openapi.TYPE_STRING
    ),
]

decline_booking_params = [
    openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="Bearer <token>",
        required=True,
        type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        'booking_id',
        openapi.IN_PATH,
        description="ID of the booking to decline",
        required=True,
        type=openapi.TYPE_INTEGER
    ),
]

# OTP Varification

send_otp_params = [
    openapi.Parameter(
        'email',
            openapi.IN_FORM,
        description="Email address to which the OTP will be sent",
        required=True,
        type=openapi.TYPE_STRING
    )
]

verify_otp_params = [
    openapi.Parameter(
        'email',
        openapi.IN_FORM,
        description="Email address associated with the OTP",
        required=True,
        type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        'otp',
        openapi.IN_FORM,
        description="OTP code received in the email",
        required=True,
        type=openapi.TYPE_STRING
    )
]

# Top Users
top_users_params = [
    openapi.Parameter(
        'Authorization',
        openapi.IN_HEADER,
        description="Bearer <token>",
        required=True,
        type=openapi.TYPE_STRING
    ),
]