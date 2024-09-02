
from app_common import models as common_models
from Blogs.models import Blogs
def all_nessasery_data(request):
    not_approvedlist = common_models.User.objects.filter(is_approved=False).count()
    not_approvedlist_rtg = common_models.User.objects.filter(is_approved=False,is_rtg = True).count()
    not_approvedlist_vendor = common_models.User.objects.filter(is_approved=False,is_vendor = True).count()
    not_approvedlist_service_provider = common_models.User.objects.filter(is_approved=False,is_serviceprovider = True).count()
    
    gardening_profile_update_obj_request = common_models.GardeningProfileUpdateRequest.objects.all().count()
    activity_request_obj = common_models.UserActivity.objects.filter(is_accepted='pending').count()
    gardener_sell_request_obj = common_models.SellProduce.objects.filter(is_approved='pending').count()
    total_blogs_from_user = Blogs.objects.filter(is_accepted = "pending").count()

    return {
        'not_approvedlist_count': not_approvedlist,
        'not_approvedlist_rtg_count': not_approvedlist_rtg,
        'not_approvedlist_vendor_count': not_approvedlist_vendor,
        'not_approvedlist_service_provider_count': not_approvedlist_service_provider,
        'gardening_profile_update_obj_request_count':gardening_profile_update_obj_request,
        'activity_request_obj_count':activity_request_obj,
        'gardener_sell_request_obj_count':gardener_sell_request_obj,
        'total_blogs_from_user_count':total_blogs_from_user
    }