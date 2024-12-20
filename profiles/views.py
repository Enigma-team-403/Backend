from django.forms import ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated

class ProfileViewSet(viewsets.ModelViewSet):
    # queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        if Profile.objects.filter(user=self.request.user).exists(): 
            return Response({"detail": "شما نمی‌توانید بیش از یک پروفایل ایجاد کنید."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer): 
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_profile(self, request):
        # نمایش پروفایل کاربر واردشده
        profile = self.get_queryset().first()
        if not profile:
            return Response({"detail": "پروفایلی برای شما یافت نشد."}, status=404)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


    
    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def edit_profile(self, request, pk=None):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


