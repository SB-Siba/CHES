import os
from django import utils
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from ..models import Blogs
from django.contrib import messages
from ..forms import BlogForm

app = "blog/rtg/"

class BlogList(View):
    model = Blogs
    template = app + "rtg_blog_list.html"

    def get(self, request):
        blog_list = self.model.objects.all().order_by('-id')
        print(blog_list)
    
        context = {
            "blog_list": blog_list,
        }
        return render(request, self.template, context)
    
class BlogAdd(View):
    model = Blogs
    form_class = BlogForm
    template = app + "rtg_blog_add.html"

    def get(self,request):
        blog_list = self.model.objects.all().order_by('-id')
        context = {
            "blog_list" : blog_list,
            "form": self.form_class,
        }
        return render(request, self.template, context)
    
    def post(self, request):

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("blogs:rtg_blog_list")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(error)
        return redirect("blogs:rtg_blog_list")

class BlogUpdate(View):
    model = Blogs
    form_class = BlogForm
    template = app + "rtg_blog_update.html"

    def get(self,request, blog_id):
        blog = self.model.objects.get(id = blog_id)
 
        context = {
            "blog" : blog,
            "form": self.form_class(instance=blog),
        }
        return render(request, self.template, context)
    
    def post(self,request, blog_id):

        blog = self.model.objects.get(id = blog_id)
        form = self.form_class(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            form.save()
            messages.success(request, f"Blog ({blog_id}) is updated successfully.....")
            return redirect(reverse('blogs:rtg_blog_list'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

        return redirect("blogs:rtg_blog_update", blog_id = blog_id)


class BlogDelete(View):
    model = Blogs

    def get(self,request, blog_id):
        blog = self.model.objects.get(id = blog_id)

        if blog.image:
            image_path = blog.image.path
            os.remove(image_path)

        blog.delete()
        messages.info(request, 'Blog is deleted succesfully......')

        return redirect("blogs:rtg_blog_list")
    
class BlogView(View):
    template_name = app + 'rtg_all_blog.html'

    def get(self, request):
        blogs = Blogs.objects.filter(is_accepted = "approved")
        context = {
            "blogs": blogs,
            }
        return render(request, self.template_name,context)
    

class BlogDetails(View):
    template_name = app + 'rtg__blog_single.html'

    def get(self, request, slug):
        blogdetail = get_object_or_404(Blogs, slug=slug)
        context = {
            'blogdetail': blogdetail,
        }
        return render(request, self.template_name, context)
    