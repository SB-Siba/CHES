from drf_yasg import openapi

pending_user_get = [
    openapi.Parameter("format", openapi.IN_QUERY, description="Response format", required=False, type=openapi.TYPE_STRING),
]

approve_user_post = [
    openapi.Parameter("pk", openapi.IN_PATH, description="User ID", required=True, type=openapi.TYPE_INTEGER),
    openapi.Parameter("coins", openapi.IN_QUERY, description="Additional coins (optional)", required=False, type=openapi.TYPE_INTEGER),
]

reject_user_delete = [
    openapi.Parameter("pk", openapi.IN_PATH, description="User ID", required=True, type=openapi.TYPE_INTEGER),
]

gardening_details_get = [
    openapi.Parameter("pk", openapi.IN_PATH, description="User ID", required=True, type=openapi.TYPE_INTEGER),
]

vendor_details_get = [
    openapi.Parameter("pk", openapi.IN_PATH, description="User ID", required=True, type=openapi.TYPE_INTEGER),
]

service_provider_details_get = [
    openapi.Parameter("pk", openapi.IN_PATH, description="User ID", required=True, type=openapi.TYPE_INTEGER),
]

quiz_answers_get = [
    openapi.Parameter("user_id", openapi.IN_PATH, description="User ID", required=True, type=openapi.TYPE_INTEGER),
]

quiz_answers_post = [
    openapi.Parameter("user_id", openapi.IN_PATH, description="User ID", required=True, type=openapi.TYPE_INTEGER),
    openapi.Parameter("quiz_points", openapi.IN_QUERY, description="Quiz Points", required=True, type=openapi.TYPE_INTEGER),
]