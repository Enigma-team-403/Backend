from django.forms import ValidationError
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

class ProfileViewSet(viewsets.ModelViewSet):

    # queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        new_user= settings.AUTH_USER_MODEL.objects.get(id = self.request.user.id)
        return Profile.objects.filter(user_id=new_user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        # نمایش پروفایل کاربر واردشده
        profile = self.get_queryset().first()
        if not profile:
            return Response({"detail": "پروفایلی برای شما یافت نشد."}, status=404)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)



# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.contrib.auth.models import User  # اضافه کردن مدل User
# from .models import Profile
# from .serializers import ProfileSerializer

# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

#     def get_queryset(self):
#         # برگرداندن تمامی پروفایل‌ها بدون احراز هویت
#         return Profile.objects.all()

#     def perform_create(self, serializer):
#         # تنظیم کاربر پیش‌فرض به جای self.request.user
#         user = User.objects.first()  # در اینجا می‌توانید کاربر پیش‌فرض را تنظیم کنید
#         serializer.save(user=user)

#     @action(detail=False, methods=['get'])
#     def my_profile(self, request):
#         # نمایش اولین پروفایل موجود در سیستم
#         profile = self.get_queryset().first()
#         if not profile:
#             return Response({"detail": "پروفایلی یافت نشد."}, status=404)
#         serializer = self.get_serializer(profile)
#         return Response(serializer.data)
