from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#import requests
from django.http import JsonResponse
import json
from admin_dashboard.serializers import NewsActivitySerializer
from app_common.error import render_error_page
from app_common.forms import NewsActivityForm
from app_common.models import NewsActivity
from helpers import utils
from django.forms.models import model_to_dict
import os
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
# for api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
# -------------------------------------------- custom import



app = "admin_dashboard/"

# ================================================== Room management ==========================================
    

@method_decorator(utils.super_admin_only, name='dispatch')
class NewsActivityList(View):
    model = NewsActivity
    template = app + "manage_newsactivity/newsactivity_list.html"

    def get(self, request):
        try:
            newsactivity_list = self.model.objects.all().order_by('-id')

            # Pagination
            paginator = Paginator(newsactivity_list, 10)  # Show 10 blogs per page
            page = request.GET.get('page')
            try:
                paginated_data = paginator.page(page)
            except PageNotAnInteger:
                paginated_data = paginator.page(1)
            except EmptyPage:
                paginated_data = paginator.page(paginator.num_pages)

            context = {
                "newsactivity_list": paginated_data,
                "paginator": paginator
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.super_admin_only, name='dispatch')
class NewsActivitySearch(View):
    model = NewsActivity
    form_class = NewsActivityForm
    template = app + "manage_newsactivity/newsactivity_list.html"

    def post(self, request):
        try:
            filter_by = request.POST.get("filter_by")
            query = request.POST.get("query")
            newsactivity_list = []

            if filter_by == "id":
                newsactivity_list = self.model.objects.filter(id=query)
            else:
                newsactivity_list = self.model.objects.filter(title__icontains=query)

            paginated_data = utils.paginate(request, newsactivity_list, 50)
            context = {
                "form": self.form_class,
                "newsactivity_list": newsactivity_list,
                "data_list": paginated_data
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


class NewsActivityFilter(View):
    model = NewsActivity
    template = app + "manage_newsactivity/newsactivity_list.html"

    def get(self, request):
        try:
            filter_by = request.GET.get("filter_by")

            if filter_by == "trending":
                newsactivity_list = self.model.objects.filter(trending="yes").order_by('-id')
            elif filter_by == "show_as_new":
                newsactivity_list = self.model.objects.filter(show_as_new="yes").order_by('-id')
            elif filter_by == "display_as_bestseller":
                newsactivity_list = self.model.objects.filter(display_as_bestseller="yes").order_by('-id')
            elif filter_by == "hide":
                newsactivity_list = self.model.objects.filter(hide="yes").order_by('-id')
            else:
                newsactivity_list = self.model.objects.filter().order_by('-id')

            paginated_data = utils.paginate(request, newsactivity_list, 50)
            context = {
                "newsactivity_list": newsactivity_list,
                "data_list": paginated_data
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.super_admin_only, name='dispatch')
class NewsActivityAdd(View):
    model = NewsActivity
    form_class = NewsActivityForm
    template = app + "manage_newsactivity/newsactivity_add.html"

    def get(self, request):
        try:
            newsactivity_list = self.model.objects.all().order_by('-id')
            context = {
                "newsactivity_list": newsactivity_list,
                "form": self.form_class,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    def post(self, request):
        try:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Newsactivity added successfully.")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

            return redirect("admin_dashboard:newsactivity_list")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.super_admin_only, name='dispatch')
class NewsActivityUpdate(View):
    model = NewsActivity
    form_class = NewsActivityForm
    template = app + "manage_newsactivity/newsactivity_update.html"

    def get(self, request, newsactivity_id):
        try:
            newsactivity = self.model.objects.get(id=newsactivity_id)
            context = {
                "newsactivity": newsactivity,
                "form": self.form_class(instance=newsactivity),
            }
            return render(request, self.template, context)
        except ObjectDoesNotExist:
            error_message = "Newsactivity not found."
            return render_error_page(request, error_message, status_code=404)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

    def post(self, request, newsactivity_id):
        try:
            newsactivity = self.model.objects.get(id=newsactivity_id)
            form = self.form_class(request.POST, request.FILES, instance=newsactivity)

            if form.is_valid():
                form.save()
                messages.success(request, f"Newsactivity ({newsactivity_id}) updated successfully.")
                return redirect(reverse('admin_dashboard:newsactivity_list'))
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

            return redirect("admin_dashboard:newsactivity_update", newsactivity_id=newsactivity_id)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


@method_decorator(utils.super_admin_only, name='dispatch')
class NewsActivityDelete(View):
    model = NewsActivity

    def get(self, request, newsactivity_id):
        try:
            newsactivity = self.model.objects.get(id=newsactivity_id)

            if newsactivity.image:
                image_path = newsactivity.image.path
                os.remove(image_path)

            newsactivity.delete()
            messages.info(request, 'Newsactivity deleted successfully.')
            return redirect("admin_dashboard:newsactivity_list")
        except ObjectDoesNotExist:
            error_message = "Blog not found."
            return render_error_page(request, error_message, status_code=404)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        


# user side

class NewsActivityView(View):
    template_name = app + 'manage_newsactivity/user_newsactivity_list.html'

    def get(self, request):
        try:
            return render(request, self.template_name)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)


class NewsActivityCategory(View):
    template_name = app + 'manage_newsactivity/user_newsactivity_list.html'

    def get(self, request):
        try:
            newsactivity = NewsActivity.objects.all()
            # highlighted_blogs = Blogs.objects.filter(is_highlight=True)
            context = {
                'newsactivity': newsactivity,
                # 'highlighted_blogs': highlighted_blogs,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)




class NewsActivityDetails(View):
    template_name = app + 'manage_newsactivity/user_newsactivity_single.html'

    def get(self, request, slug):
        try:
            newsactivitydetail = get_object_or_404(NewsActivity, slug=slug)
            context = {
                'newsactivitydetail': newsactivitydetail,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
        
#API 

class NewsActivityListAPIView(APIView):

    @swagger_auto_schema(
        tags=["NewsActivity"],
        operation_description="Retrieve all NewsActivity posts.",
        responses={200: 'Successful response with all NewsActivity '}
    )
    def get(self, request):
        newsactivity = NewsActivity.objects.all()
        serializer = NewsActivitySerializer(newsactivity, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NewsActivityDetailsAPIView(APIView):

    @swagger_auto_schema(
        tags=["NewsActivity"],
        operation_description="Retrieve NewsActivity details by slug.",
        responses={
            200: 'Successful response with NewsActivity details',
            404: 'Blog post not found'
        }
    )
    def get(self, request, slug):
        newsactivity = get_object_or_404(NewsActivity, slug=slug)
        serializer = NewsActivitySerializer(newsactivity)
        return Response(serializer.data, status=status.HTTP_200_OK)