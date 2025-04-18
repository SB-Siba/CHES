from rest_framework import serializers
from app_common import models as common_models

class PendingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.User
        fields = ['id', 'full_name', 'email', 'is_rtg', 'is_vendor', 'is_serviceprovider']


class AdminSiteGardeningProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.GardeningProfile
        fields = '__all__'

class VendorDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.VendorDetails
        fields = '__all__'

class ServiceProviderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.ServiceProviderDetails
        fields = '__all__'

class QuizAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.GaredenQuizModel
        fields = '__all__'

class NewsActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.NewsActivity
        fields = '__all__'

class MediaGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.MediaGallery
        fields = '__all__'