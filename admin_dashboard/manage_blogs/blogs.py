import os
from django import utils
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from Blogs.models import Blogs
from django.contrib import messages
from Blogs.forms import BlogForm
from django.db.models import Q

from app_common.error import render_error_page

app = "admin_dashboard/manage_blogs/"


class AllBlogsFromUsers(View):
    model = Blogs
    template = app + "all_blogs_from_user.html"

    def get(self, request):
        try:
            blogs = self.model.objects.all()
            context = {
                'blog_list': blogs
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message)


class ApproveBlog(View):
    model = Blogs

    def get(self, request, blog_id):
        try:
            blog = self.model.objects.get(id=blog_id)
            blog.is_accepted = "approved"
            blog.save()
            return redirect(reverse('admin_dashboard:blogs_list'))
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message)


class DeclineBlog(View):
    model = Blogs

    def get(self, request, blog_id):
        try:
            blog = self.model.objects.get(id=blog_id)
            blog.is_accepted = "rejected"
            blog.save()
            return redirect(reverse('admin_dashboard:blogs_list'))
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message)


class DeleteBlog(View):
    model = Blogs

    def get(self, request, blog_id):
        try:
            self.model.objects.get(id=blog_id).delete()
            return redirect(reverse('admin_dashboard:blogs_list'))
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message)


class BlogSearch(View):
    model = Blogs
    template = app + "all_blogs_from_user.html"

    def post(self, request):
        try:
            query = request.POST.get('query', '')
            filter_by = request.POST.get('filter_by', 'all')

            if filter_by == "id":
                blog_list = self.model.objects.filter(id=query)
            elif filter_by == "name":
                blog_list = self.model.objects.filter(title__icontains=query)
            elif filter_by == "all":
                blog_list = self.model.objects.filter(
                    Q(id__icontains=query) | Q(title__icontains=query)
                )
            context = {
                "blog_list": blog_list,
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message)


class BlogUpdate(View):
    model = Blogs
    form_class = BlogForm
    template = app + "blog_update.html"

    def get(self, request, blog_id):
        try:
            blog = get_object_or_404(self.model, id=blog_id)
            context = {
                "blog": blog,
                "form": self.form_class(instance=blog),
            }
            return render(request, self.template, context)
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message)

    def post(self, request, blog_id):
        try:
            blog = self.model.objects.get(id=blog_id)
            form = self.form_class(request.POST, request.FILES, instance=blog)

            if form.is_valid():
                form.save()
                messages.success(request, f"Blog ({blog_id}) is updated successfully.")
                return redirect(reverse('admin_dashboard:blogs_list'))
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
                return redirect("admin_dashboard:blog_update", blog_id=blog_id)

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            return render_error_page(request, error_message)