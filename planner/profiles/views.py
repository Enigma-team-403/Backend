from django.forms import ValidationError
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # فقط پروفایل کاربر واردشده را برمی‌گرداند
        user = self.request.user
        if not user.is_authenticated:
            return Profile.objects.none()
        return Profile.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_profile(self, request):
        # نمایش پروفایل کاربر واردشده
        profile = self.get_queryset().first()
        if not profile:
            return Response({"detail": "پروفایلی برای شما یافت نشد."}, status=404)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


