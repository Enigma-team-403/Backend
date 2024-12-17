
from community.serializers import CommunitySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from community.models import Community  # فرض کنید مدل Community در اپلیکیشن community است.

class AddMemberToCommunity(APIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def post(self, request, community_id):
        # یافتن کامیونیتی بر اساس ID
        community = get_object_or_404(Community, id=community_id)

        # بررسی اینکه آیا کاربر درخواست‌دهنده سازنده کامیونیتی است
        if community.creator != request.user:
            return Response({"detail": "You are not authorized to add members to this community."}, status=status.HTTP_403_FORBIDDEN)

        # گرفتن ID کاربر مورد نظر از درخواست
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # یافتن کاربر بر اساس ID
        user_to_add = get_object_or_404(User, id=user_id)

        # اضافه کردن کاربر به لیست اعضای کامیونیتی
        community.members.add(user_to_add)

        return Response({"detail": "User added successfully to the community."}, status=status.HTTP_200_OK)
