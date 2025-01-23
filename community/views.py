from requests import Response
from rest_framework import viewsets, permissions
from .models import Community, Category ,MembershipRequest
from .serializers import CommunitySerializer, DetailsSerializer, HabitSerializer,MembershipRequestSerializer, ApproveMembershipRequestSerializer,AddMemberSerializer,CategorySerializer,CommunityMemberSerializer
from HabitTracker.models import Habit
from rest_framework.decorators import action , api_view ,permission_classes
from rest_framework.response import Response
from HabitTracker.serializers import HabitSerializer
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter        
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CommunityFilter
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import requests

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=['get'], url_path='list-Category')    
    def list_tags(self, request):
        categories = self.queryset.all()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

class SearchCommunityView(APIView):
    def get(self, request):
        query = request.query_params.get('title', '').strip()
        if not query:
            return Response({"error": "Please provide a name to search."}, status=status.HTTP_400_BAD_REQUEST)

        communities = Community.objects.filter(title__icontains=query)  
        if not communities.exists():
            return Response({"error": "No communities found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommunityFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Community Name')
    category = CharFilter(field_name='category__name', lookup_expr='icontains', label='Category Name')


    class Meta:
        model = Community
        fields = ['name', 'category']

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated] 
    
    filter_backends = [DjangoFilterBackend] 
    filterset_class = CommunityFilter
    search_fields = ['title']
    filterset_fields = ['category']





    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # اینجا کاربر را تنظیم می‌کنیم

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return Response({"error": "Authentication required."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        communities = Community.objects.all()
        serializer = self.get_serializer(communities, many=True)
        return Response(serializer.data)    
    
    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def linked_habits(self, request, pk=None):
        community = self.get_object()

        if request.method == 'GET':
            habits = community.external_habits.all()
            serializer = HabitSerializer(habits, many=True)
            return Response(serializer.data)

        if request.method == 'POST':
            habit_id = request.data.get('habit_id')
            if not habit_id:
                return Response({"detail": "habit_id is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                habit = Habit.objects.get(id=habit_id)
            except Habit.DoesNotExist:
                return Response({"detail": "Habit not found."}, status=status.HTTP_404_NOT_FOUND)

            community.external_habits.add(habit)
            return Response({"detail": "Habit added successfully."}, status=status.HTTP_201_CREATED)
    
    def perform_update(self, serializer):
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        community = self.get_object() 
        serializer = self.get_serializer(community)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        community = self.get_object()
        serializer = self.get_serializer(community, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        community = self.get_object()
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

    @action(detail=True, methods=['post'])#, permission_classes=[permissions.IsAuthenticated])
    def add_habits(self, request, pk=None):
        community = self.get_object()         
        habit_ids = request.data.get('habit_ids', [])
        habits_to_add = Habit.objects.filter(id__in=habit_ids, user=request.user)
        if len(habits_to_add) != len(habit_ids): 
            return Response({"detail": "Some habits not found."}, status=status.HTTP_400_BAD_REQUEST) 
        community.habits.add(*habits_to_add) 
        return Response({"detail": "Habits added successfully."}, status=status.HTTP_200_OK)
        

    @action(detail=True, methods=['GET', 'PUT'])
    def details(self, request, pk=None):
        community = self.get_object()
        if request.method == 'GET':
            serializer = DetailsSerializer(community)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = DetailsSerializer(community, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'])
    def add_members(self, request, pk=None):
        community = self.get_object()
        user_id = request.data.get('user_id')
        print(f"User ID received: {user_id}")
        try:
            user = User.objects.get(user_id=user_id)
            print(f"User found: {user}")
        except User.DoesNotExist:
            print("User not found.")
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        membership_request = MembershipRequest.objects.create(community=community, requester=user,status='pending' )
        return Response({"detail": "Membership request sent successfully."}, status=status.HTTP_201_CREATED)
        # community.members.add(user)
        # return Response({"detail": "Member added successfully."}, status=status.HTTP_200_OK)
        

    @action(detail=True, methods=['get'])
    def membership_requests(self, request, pk=None):
        community = self.get_object()
        user = request.user
        # تشخیص سازنده‌ی کامیونیتی بدون نیاز به احراز هویت
        if community.user and community.user != user:
            return Response({"detail": "Only the community admin can view membership requests."}, status=status.HTTP_403_FORBIDDEN)

        membership_requests = MembershipRequest.objects.filter(community=community)
        serializer = MembershipRequestSerializer(membership_requests, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def accept_membership_request(self, request, pk=None):
        community = self.get_object()
        user = request.user
        request_id = request.data.get('request_id')
        selected_habit_id = request.data.get('selected_habit_id')
        # تشخیص سازنده‌ی کامیونیتی بدون نیاز به احراز هویت
        if community.user and community.user != user:
            return Response({"detail": "Only the community admin can accept membership requests."}, status=status.HTTP_403_FORBIDDEN)

        try:
            membership_request = MembershipRequest.objects.get(id=request_id, community=community)
            selected_habit = Habit.objects.get(id=selected_habit_id)
            membership_request.status = 'accepted'
            membership_request.selected_habit = selected_habit
            membership_request.save()

            community.members.add(membership_request.requester)
            return Response({"detail": "Membership request accepted and user added to community."}, status=status.HTTP_200_OK)
        except MembershipRequest.DoesNotExist:
            return Response({"detail": "Membership request not found."}, status=status.HTTP_404_NOT_FOUND)
        except Habit.DoesNotExist:
            return Response({"detail": "Selected habit not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        community = self.get_object()
        members = community.members.all()
        serializer = CommunityMemberSerializer(members, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def member_progress(self, request, pk=None):
        community = self.get_object()
        members = community.members.all()
        response_data = []

        for member in members:
            habits = member.tracker_habits.all()
            habit_data = []

            for habit in habits:
                daily_progress = habit.daily_progress.all()
                completed_days = daily_progress.filter(completed=True).count()
                progress_percentage = (completed_days / habit.duration) * 100 if habit.duration > 0 else 0
                habit_data.append({
                    'habit_id': habit.id,
                    'habit_name': habit.name,
                    'progress_percentage': progress_percentage,
                })
            
            response_data.append({
                'member_id': member.user_id,
                'username': member.username,
                'profile_picture': member.profile.profile_picture.url if member.profile.profile_picture else None,
                'habits': habit_data,
            })
        
        return Response(response_data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated]) 
    def my_communities(self, request, pk=None): 
        user = request.user 
        communities = Community.objects.filter(user=user) 
        serializer = CommunitySerializer(communities, many=True) 
        return Response(serializer.data) 
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated]) 
    def joined_communities(self, request, pk=None): 
        user = request.user 
        communities = Community.objects.filter(members=user) 
        serializer = CommunitySerializer(communities, many=True) 
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def recommended_communities(self, request):
        user_interests = request.user.interests.values_list('interest__id', flat=True)
        communities = Community.objects.filter(categories__id__in=user_interests).distinct()
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_community_habit_progress(request, community_id):
    membership_request = MembershipRequest.objects.filter(community_id=community_id, requester=request.user).first()
    if not membership_request:
        return Response({"detail": "Membership request not found."}, status=404)

    selected_habit = membership_request.selected_habit
    if not selected_habit:
        return Response({"detail": "Selected habit not found."}, status=404)

    update_progress_url = 'http://localhost:8000/update-progress/'
    data = {
        'progress_id': request.data.get('progress_id'),
        'completed': request.data.get('completed')
    }
    response = requests.post(update_progress_url, json=data)

    if response.status_code == 200:
        return Response(response.json(), status=200)
    else:
        return Response(response.json(), status=response.status_code)


def community_list_view(request):
    communities = Community.objects.all()
    return render(request, 'community_list.html', {'communities': communities})


class UserHabitViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    @action(detail=False, methods=['get'], url_path='list-Habits')    
    def list_habits(self, request):
        habits = self.queryset.all()
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)
    
    def get(self, request):
        user_habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(user_habits, many=True)
        return Response(serializer.data)

class UserMembershipRequestsView(APIView):
    queryset = MembershipRequest.objects.all()
    serializer_class = MembershipRequestSerializer


    def get(self, request):
        if request.user.is_anonymous:
            return Response({"detail": "Anonymous user cannot access this information."}, status=status.HTTP_400_BAD_REQUEST)
        
        membership_requests = MembershipRequest.objects.filter(requester=request.user)
        serializer = MembershipRequestSerializer(membership_requests, many=True)
        return Response(serializer.data)

class MembershipRequestViewSet(viewsets.ModelViewSet):
    queryset = MembershipRequest.objects.all()
    serializer_class = MembershipRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # برگرداندن درخواست‌های عضویت برای کاربر فعلی
        return self.queryset.filter(requester=self.request.user)

    def create(self, request, *args, **kwargs):
        # اضافه کردن کاربر فعلی به درخواست عضویت
        data = request.data.copy()
        data['requester'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_membership_request(request):
    community_id = request.data.get('community_id')
    selected_habit_id = request.data.get('selected_habit_id')
    requester = request.user

    # بررسی وجود درخواست عضویت مشابه
    if MembershipRequest.objects.filter(community_id=community_id, requester=requester).exists():
        return Response({"detail": "Membership request already exists."}, status=status.HTTP_400_BAD_REQUEST)

    # اگر درخواست مشابه وجود ندارد، ایجاد درخواست جدید
    serializer = MembershipRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        membership_request = serializer.save()
        response_serializer = MembershipRequestSerializer(membership_request)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_membership_requests(request, community_id):
    try:
        community = Community.objects.get(id=community_id)
        # تشخیص سازنده‌ی کامیونیتی بدون نیاز به احراز هویت
        if community.user and community.user != request.user:
            return Response({"detail": "Only the community admin can view membership requests."}, status=status.HTTP_403_FORBIDDEN)

        membership_requests = MembershipRequest.objects.filter(community=community)
        serializer = MembershipRequestSerializer(membership_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Community.DoesNotExist:
        return Response({"detail": "Community not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manage_membership_request(request, community_id):
    serializer = ApproveMembershipRequestSerializer(data=request.data)
    if serializer.is_valid():
        request_id = serializer.validated_data['request_id']
        action = serializer.validated_data['action']

        try:
            community = Community.objects.get(id=community_id)
            # تشخیص سازنده‌ی کامیونیتی بدون نیاز به احراز هویت
            if community.user and community.user != request.user:
                return Response({"detail": "Only the community admin can manage membership requests."}, status=status.HTTP_403_FORBIDDEN)

            membership_request = MembershipRequest.objects.get(id=request_id, community=community)
            if action == 'approve':
                membership_request.status = 'approved'
                community.members.add(membership_request.requester)
                membership_request.save()
                return Response({"detail": "Membership request approved and user added to community."}, status=status.HTTP_200_OK)
            elif action == 'reject':
                membership_request.status = 'rejected'
                membership_request.save()
                return Response({"detail": "Membership request rejected."}, status=status.HTTP_200_OK)
        except Community.DoesNotExist:
            return Response({"detail": "Community not found."}, status=status.HTTP_404_NOT_FOUND)
        except MembershipRequest.DoesNotExist:
            return Response({"detail": "Membership request not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

