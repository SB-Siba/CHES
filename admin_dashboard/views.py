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
        profile_update_obj = common_models.GardeningProfileUpdateRequest.objects.all()
        activity_request_obj = common_models.UserActivity.objects.filter(is_accepted='pending').order_by('-date_time')
        gardener_sell_request_obj = common_models.SellProduce.objects.filter(is_approved='pending').order_by('-date_time')

        return render(request, self.template,locals())

