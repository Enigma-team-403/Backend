from rest_framework import serializers
from .models import Profile

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = '__all__'
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'email', 'username', 'birth_date', 
                  'interesting', 'job', 'city', 'country', 'bio', 'profile_picture']
