from rest_framework import viewsets, permissions
from .models import Interest, UserInterest
from .serializers import InterestSerializer, UserInterestSerializer
from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from .models import UserInterest, Interest
from .serializers import UserInterestSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAuthenticated]




from rest_framework import viewsets, permissions
from .models import UserInterest, Interest
from .serializers import UserInterestSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

class UserInterestViewSet(viewsets.ModelViewSet):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserInterest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def save_user_interests(self, request):
        selected_interests = request.data.get('interests')
        if not isinstance(selected_interests, list) or not 2 <= len(selected_interests) <= 3:
            return Response({'error': 'Please select 2 or 3 interests.'}, status=400)

        UserInterest.objects.filter(user=request.user).delete()  # Clear previous interests
        for interest_id in selected_interests:
            interest = Interest.objects.get(id=interest_id)
            UserInterest.objects.create(user=request.user, interest=interest)

        return Response({'message': 'Interests saved successfully.'}, status=201)


def select_interests(request):
    if request.method == 'POST':
        selected_interests = request.POST.getlist('interests')
        if len(selected_interests) < 2 or len(selected_interests) > 3:
            return render(request, 'interest/select_interests.html', {'interests': Interest.objects.all(), 'error': 'Please select 2 or 3 interests.'})
        
        UserInterest.objects.filter(user=request.user).delete()  # Clear previous interests
        for interest_id in selected_interests:
            interest = Interest.objects.get(id=interest_id)
            UserInterest.objects.create(user=request.user, interest=interest)
        return redirect('recommended-communities')

    interests = Interest.objects.all()
    return render(request, 'interest/select_interests.html', {'interests': interests})
