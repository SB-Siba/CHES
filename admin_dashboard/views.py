from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from app_common import models as common_models
from django.utils.decorators import method_decorator

from helpers import utils

app = "admin_dashboard/"

@method_decorator(utils.super_admin_only, name='dispatch')
class AdminDashboard(View):
    template = app + "index.html"

    def get(self, request):
        not_approvedlist = common_models.User.objects.filter(is_approved=False).order_by('-id')
        not_approvedlist_rtg = common_models.User.objects.filter(is_approved=False,is_rtg = True).order_by('-id')
        not_approvedlist_vendor = common_models.User.objects.filter(is_approved=False,is_vendor = True).order_by('-id')
        not_approvedlist_service_provider = common_models.User.objects.filter(is_approved=False,is_serviceprovider = True).order_by('-id')

        profile_update_obj = common_models.GardeningProfileUpdateRequest.objects.all()
        activity_request_obj = common_models.UserActivity.objects.filter(is_accepted='pending').order_by('-date_time')
        gardener_sell_request_obj = common_models.SellProduce.objects.filter(is_approved='pending').order_by('-date_time')

        total_rt_gardeners = common_models.User.objects.filter(is_rtg = True).count()
        total_vendors = common_models.User.objects.filter(is_vendor = True).count()
        total_service_provider = common_models.User.objects.filter(is_serviceprovider = True).count()
        total_activities = common_models.UserActivity.objects.all().count()
        rtg_garden_profile = common_models.GardeningProfile.objects.all()
        rtg_total_garden_area = sum([i.garden_area for i in rtg_garden_profile])
        rtg_total_plants = sum([i.number_of_plants for i in rtg_garden_profile])

        return render(request, self.template,locals())

