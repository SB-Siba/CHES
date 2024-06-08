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
    openapi.Parameter("service_type", openapi.IN_QUERY, description="Service Type", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("service_area", openapi.IN_QUERY, description="Service Area", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("average_cost_per_hour", openapi.IN_QUERY, description="Average Cost Per Hour", required=True, type=openapi.TYPE_NUMBER),
    openapi.Parameter("years_experience", openapi.IN_QUERY, description="Years of Experience", required=True, type=openapi.TYPE_INTEGER),
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

give_comment_post = [
    openapi.Parameter("Authorization", openapi.IN_HEADER, description="Bearer <token>", required=True, type=openapi.TYPE_STRING),
    openapi.Parameter("post_id", openapi.IN_FORM, description="ID of the post to comment on", required=True, type=openapi.TYPE_INTEGER),
    openapi.Parameter("comment", openapi.IN_FORM, description="Comment content", required=True, type=openapi.TYPE_STRING),
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