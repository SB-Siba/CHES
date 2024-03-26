from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator

from helpers import utils

app = "user_dashboard/"

#@method_decorator(utils.login_required, name='dispatch')
class UserDashboard(View):
    template = app + "index.html"

    def get(self, request):
        return render(request, self.template)

