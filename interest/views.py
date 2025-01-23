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

    def create(self, request, *args, **kwargs):  
        selected_interests = request.data.get('interests')
        if not isinstance(selected_interests, list) or len(selected_interests) == 0:
            return Response({'error': 'Please provide a list of interest IDs.'}, status=400)
        UserInterest.objects.filter(user=request.user).delete()  # Clear previous interests
        
        for interest_id in selected_interests:
            try: 
                interest = Interest.objects.get(id=interest_id) 
                UserInterest.objects.create(user=request.user, interest=interest) 
            except Interest.DoesNotExist: 
                return Response({'error': f'Interest with id {interest_id} does not exist.'}, status=400)
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
