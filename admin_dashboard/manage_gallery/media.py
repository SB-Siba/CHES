from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from app_common.forms import MediaGalleryForm
from app_common.models import MediaGallery

app = "admin_dashboard/manage_gallery/"

class MediaGalleryListView(View):
    template = app + 'media_gallery_list.html'

    def get(self, request):
        media_items = MediaGallery.objects.all()
        form = MediaGalleryForm()
        return render(request, self.template, {'form': form, 'media_items': media_items})

    def post(self, request):
        form = MediaGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('media_image')  # Retrieve list of files
            for image in images:
                MediaGallery.objects.create(media_image=image)  # Save each file as a new instance
            messages.success(request, "Images added successfully.")
        else:
            messages.error(request, "Error adding images.")
        return redirect('admin_dashboard:media_gallery_list')

class MediaGalleryDeleteView(View):
    def post(self, request, pk):
        media_item = get_object_or_404(MediaGallery, pk=pk)
        media_item.delete()
        messages.success(request, "Image deleted successfully.")
        return redirect('admin_dashboard:media_gallery_list')