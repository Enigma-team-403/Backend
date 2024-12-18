from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']  # کاربر فقط خواندنی باشد



#http://127.0.0.1:8000/api/profiles/profiles/my_profile/ :: مشاهده پروفایل خود کاربر
#http://127.0.0.1:8000/api/profiles/profiles/<id>/  ::ویرایش پروفایل
#http://127.0.0.1:8000/api/profiles/profiles/ :: ایجاد پروفایل
#http://127.0.0.1:8000/api/profiles/profiles    :: لیست کردن پروفایل‌ها

