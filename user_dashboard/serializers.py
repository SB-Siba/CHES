from rest_framework import serializers
from app_common import models

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['full_name', 'email', 'password', 'confirm_password', 'contact', 'city']

class GardeningDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GardeningProfile
        fields = ['garden_area', 'number_of_plants', 'number_of_unique_plants', 'garden_image']

class GardenQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GaredenQuizModel
        fields = ['user', 'questionANDanswer']
