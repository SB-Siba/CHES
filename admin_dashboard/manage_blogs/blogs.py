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

app = "admin_dashboard/manage_blogs/"


class AllBlogsFromUsers(View):
    model = Blogs
    template = app + "all_blogs_from_user.html"
    def get(self, request):
        blogs = self.model.objects.all()
        context = {
            'blog_list': blogs
        }
        return render(request, self.template,context)
    
class ApproveBlog(View):
    model = Blogs
    print("lklk")
    def get(self,request,blog_id):
        blog = self.model.objects.get(id=blog_id)
        blog.is_accepted = "approved"
        blog.save()
        return redirect(reverse('admin_dashboard:blogs_list'))
    
class DeclineBlog(View):
    model = Blogs

    def get(self,request,blog_id):
        blog = self.model.objects.get(id=blog_id)
        blog.is_accepted = "rejected"
        blog.save()
        return redirect(reverse('admin_dashboard:blogs_list'))
    
class DeleteBlog(View):
    model = Blogs

    def get(self,request,blog_id):
        blog = self.model.objects.get(id=blog_id).delete()
        return redirect(reverse('admin_dashboard:blogs_list'))
    

class BlogSearch(View):
    model = Blogs
    template = app + "all_blogs_from_user.html"

    def post(self,request):
        query = request.POST.get('query', '')
        filter_by = request.POST.get('filter_by', 'all')

        if filter_by == "id":
            blog_list = self.model.objects.filter(id = query)
        elif filter_by == "name":
            blog_list = self.model.objects.filter(title__icontains = query)
        elif filter_by == "all":
            blog_list = self.model.objects.filter(
                Q(id__icontains=query) | Q(title__icontains=query)
            )
        context = {
            "blog_list":blog_list,
        }
        return render(request, self.template, context)