from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from admin_dashboard.serializers import MediaGallerySerializer
from app_common.forms import MediaGalleryForm
from app_common.models import MediaGallery
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

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
    
#API views


class GalleryAPIView(APIView):
  
    @swagger_auto_schema(
        tags=["NewsActivity"],
        operation_description="Retrieve all Gallery posts.",
        responses={200: 'Successful response with all Gallery '}
    )

    def get(self, request, *args, **kwargs):
        try:
            media_items = MediaGallery.objects.all()
            serializer = MediaGallerySerializer(media_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = {'error': f"An unexpected error occurred: {str(e)}"}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)