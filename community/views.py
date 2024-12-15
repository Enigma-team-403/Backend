from requests import Response
from rest_framework import viewsets, permissions
from .models import Community, Category, Habit
from .serializers import CommunitySerializer, CategorySerializer, HabitSerializer

from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.views import View


from django.shortcuts import render, redirect
from django.views import View
from .models import Community
from .forms import CommunityForm  # A form to handle community creation


from django.contrib.auth import get_user_model

User = get_user_model()




class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    @action(detail=True, methods=['get'], url_path='user-progress')
    def user_progress(self, request, pk=None):
        community = self.get_object()
        users = community.users.all()  # Get all users in the community
        user_data = [{'username': user.username, 'email': user.email} for user in users]
        return Response(user_data)
        # users = User.objects.filter(habits__communities=community).distinct()
        
        user_progress_data = []
        for user in users:
            # Get the progress for the user's habit(s)
            user_habits = Habit.objects.filter(user=user, communities=community)
            progress_percentages = []
            for habit in user_habits:
                completed_days = habit.daily_progress.filter(completed=True).count()
                progress_percentage = (completed_days / habit.duration) * 100
                progress_percentages.append({'habit': habit.name, 'progress': progress_percentage})

            user_progress_data.append({
                'user': user.username,
                'progress': progress_percentages
            })

        return Response(user_progress_data)
    
class UpdateCommunityView(View):
    def get(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        form = CommunityForm(instance=community)
        return render(request, 'community/update_community.html', {'form': form, 'community': community})

    def post(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        form = CommunityForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            return redirect('community-detail', community_id=community.id)
        return render(request, 'community/update_community.html', {'form': form, 'community': community})


class CreateCommunityView(View):
    def get(self, request):
        form = CommunityForm()
        return render(request, 'community/create_community.html', {'form': form})

    def post(self, request):
        form = CommunityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community-list')  # Redirect to the community list after creation
        return render(request, 'community/create_community.html', {'form': form})


class DeleteCommunityView(View):
    def get(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        return render(request, 'community/delete_community.html', {'community': community})

    def post(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        community.delete()
        return redirect('community-list')

class CommunityDetailView(View):
    def get(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        return render(request, 'community/delete_community.html', {'community': community})




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserHabitViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data)
    
class RegisterUserView(View):
    def get(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        return render(request, 'community/register_user.html', {'community': community})

    def post(self, request, community_id):
        community = get_object_or_404(Community, id=community_id)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Create user and add to the community
        user = User.objects.create_user(username=username, email=email, password=password)
        community.users.add(user)  # Add user to community
        return redirect('community-detail', community_id=community.id)
    
class CommunityListView(View):
    def get(self, request):
        communities = Community.objects.all()
        return render(request, 'community/community_list.html', {'communities': communities})
