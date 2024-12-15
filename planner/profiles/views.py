from rest_framework import viewsets
from .models import Profile
from .serializers import ProfileSerializer


from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    

class UserDetailView(APIView):
    def get(self, request, username):
        profile = Profile.objects.filter(user__username=username).first()
        if profile is None:
            return Response({'detail': 'User not found.'}, status=404)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
