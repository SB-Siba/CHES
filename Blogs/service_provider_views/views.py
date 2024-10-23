import os
from django import utils
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from helpers import utils
from helpers.decorators import login_required
from app_common.error import render_error_page
from ..models import Blogs
from django.contrib import messages
from ..forms import BlogForm
from django.db.models import Q

app = "blog/serviceprovider/"

@method_decorator(utils.login_required, name='dispatch')
class SpBlogList(View):
    model = Blogs
    template = app + "sp_blog_list.html"

    def get(self, request):
        try:
            blog_list = self.model.objects.filter(user = request.user).order_by('-id')
        
            context = {
                "blog_list": blog_list,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    
@method_decorator(utils.login_required, name='dispatch')
class SpBlogAdd(View):
    model = Blogs
    form_class = BlogForm
    template = app + "sp_blog_add.html"

    def get(self,request):
        try:
            blog_list = self.model.objects.all().order_by('-id')
            context = {
                "blog_list" : blog_list,
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
                blog = form.save(commit=False)
                blog.user = request.user  # Set the current user as the author
                blog.save()
                return redirect("blogs:sp_blog_list")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        print(error)
            return redirect("blogs:sp_blog_list")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class SpBlogUpdate(View):
    model = Blogs
    form_class = BlogForm
    template = app + "sp_blog_update.html"

    def get(self,request, blog_id):
        try:
            blog = get_object_or_404(self.model, id=blog_id)
    
            context = {
                "blog" : blog,
                "form": self.form_class(instance=blog),
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    
    def post(self,request, blog_id):
        try:
            blog = self.model.objects.get(id = blog_id)
            form = self.form_class(request.POST, request.FILES, instance=blog)

            if form.is_valid():
                form.save()
                messages.success(request, f"Blog ({blog_id}) is updated successfully.....")
                return redirect(reverse('blogs:sp_blog_list'))
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')

            return redirect("blogs:sp_blog_update", blog_id = blog_id)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)

@method_decorator(utils.login_required, name='dispatch')
class SpBlogDelete(View):
    model = Blogs

    def get(self,request, blog_id):
        try:
            blog = self.model.objects.get(id = blog_id)

            if blog.image:
                image_path = blog.image.path
                os.remove(image_path)

            blog.delete()

            return redirect("blogs:sp_blog_list")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    
@method_decorator(utils.login_required, name='dispatch')
class SpBlogView(View):
    template_name = app + 'sp_all_blog.html'

    def get(self, request):
        try:
            blogs = Blogs.objects.filter(is_accepted = "approved")
            context = {
                "blogs": blogs,
                }
            return render(request, self.template_name,context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    

@method_decorator(utils.login_required, name='dispatch')
class SpBlogDetails(View):
    template_name = app + 'sp_blog_single.html'

    def get(self, request, slug):
        try:
            blogdetail = get_object_or_404(Blogs, slug=slug)
            context = {
                'blogdetail': blogdetail,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message, status_code=400)
    

@method_decorator(utils.login_required, name='dispatch')
class SPBlogSearch(View):
    model = Blogs
    template = app + "sp_blog_list.html"

    def post(self, request):
        try:
            query = request.POST.get('query', '')
            filter_by = request.POST.get('filter_by', 'all')

            if filter_by == "id":
                blog_list = self.model.objects.filter(id=query,user = request.user)
            elif filter_by == "name":
                blog_list = self.model.objects.filter(title__icontains=query,user = request.user)
            elif filter_by == "all":
                blog_list = self.model.objects.filter(
                    Q(id__icontains=query) | Q(title__icontains=query),
                    user=request.user
                )
            context = {
                "blog_list": blog_list,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message)