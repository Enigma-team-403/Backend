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
from django.db import models    
from interest.models import Interest, UserInterest  # فرض کنید مدل علاقه‌مندی‌ها در اپ interest وجود دارد
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
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

        data = request.data.copy()
        if 'members' not in data or not data['members']:
            data['members'] = [user.id]

        habit_ids = data.get('habits', [])
        selected_habit = None
        if habit_ids:
            try:
                selected_habit = Habit.objects.get(id=habit_ids[0])
            except Habit.DoesNotExist:
                return Response({"error": "Selected habit does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        community = serializer.save()

        MembershipRequest.objects.create(
            community=community,
            requester=user,
            selected_habit=selected_habit,
            status='accepted'
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='update_profile_picture')
    def update_profile_picture(self, request, pk=None):
        community = self.get_object()
        serializer = self.get_serializer(community, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
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

        if not selected_habit_id:
            return Response({"detail": "A habit must be selected to join the community."}, status=status.HTTP_400_BAD_REQUEST)

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


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import requests

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        community = self.get_object()
        members = community.members.all()
        response_data = []

        for member in members:
            profile = member.profile  # دریافت پروفایل کاربر
            membership_request = MembershipRequest.objects.filter(community=community, requester=member).first()
            if membership_request and membership_request.selected_habit:
                selected_habit = membership_request.selected_habit

                # ارسال درخواست به اندپوینت /habits/ برای دریافت پروگرس هبیت
                habit_details_url = f'https://shadizargar.pythonanywhere.com/api/habits/habits{selected_habit.id}/'
                try:
                    response = requests.get(habit_details_url)
                    response.raise_for_status()
                    habit_data = response.json()
                    progress_percentage = habit_data.get('progress', 0)  # دریافت پروگرس از پاسخ

                    habit_info = {
                        'id': selected_habit.id,
                        'name': selected_habit.name,
                        'progress_percentage': progress_percentage,
                    }
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching habit progress: {e}")
                    habit_info = None
            else:
                habit_info = None

            response_data.append({
                'member_id': member.pk,
                'username': member.username,
                'profile_picture': profile.profile_picture.url if profile.profile_picture else None,  # افزودن عکس پروفایل
                'selected_habit': habit_info,
            })

        return Response(response_data)

    @action(detail=False, methods=['get'], url_path='recommended_communities')
    def recommended_communities(self, request):
        user = request.user
        # دریافت علاقمندی‌های کاربر از مدل UserInterest
        user_interests = UserInterest.objects.filter(user=user).values_list('interest__name', flat=True)

        # فیلتر کردن کامیونیتی‌ها بر اساس هبیت‌های مرتبط با علاقمندی‌های کاربر
        recommended_communities = Community.objects.filter(habits__name__in=user_interests).distinct()
        serializer = self.get_serializer(recommended_communities, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=['get'], url_path='my_communities')
    def my_communities(self, request):
        user = request.user
        # یافتن کامیونیتی‌هایی که کاربر عضو آنها است یا آنها را ایجاد کرده است
        communities = Community.objects.filter(models.Q(members=user) | models.Q(user=user)).distinct()
        serializer = self.get_serializer(communities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='joined_communities')
    def joined_communities(self, request):
        user = request.user
        # یافتن کامیونیتی‌هایی که کاربر عضو آنها است
        communities = Community.objects.filter(members=user).distinct()
        serializer = self.get_serializer(communities, many=True)
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from community.models import MembershipRequest
from HabitTracker.models import DailyProgress, Habit
from django.utils.timezone import now
import requests

class UpdateCommunityHabitProgressView(APIView):
    def post(self, request, community_id, format=None):
        habit_id = request.data.get('habit_id')
        completed = request.data.get('completed', False)  # مقدار پیش‌فرض False

        habit = get_object_or_404(Habit, id=habit_id)
        current_date = now().date()

        daily_progress, created = DailyProgress.objects.get_or_create(habit=habit, date=current_date)

        if completed:
            daily_progress.completed_amount = habit.daily_target  # اگر انجام شد، مقدار daily_target اضافه شود
        else:
            daily_progress.completed_amount = 0  # اگر انجام نشد، مقدار صفر باشد

        daily_progress.save()

        # به‌روزرسانی پروگرس عادت
        progress_increase = (habit.daily_target / habit.goal) * 100 if habit.goal > 0 else 0
        habit.progress = min(habit.progress + progress_increase, 100)  # افزایش پروگرس، حداکثر تا 100
        habit.save()

        # ارسال درخواست به‌روزرسانی به اپ هبیت
        update_progress_url = 'http://127.0.0.1:8000/api/habit/update_progress/'  # مطمئن شوید که این URL صحیح است
        data = {
            'habit_id': habit.id,
            'completed': daily_progress.completed_amount > 0
        }
        try:
            response = requests.post(update_progress_url, json=data)
            response.raise_for_status()
            print("Habit progress updated in Habit Tracker successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error updating habit progress in Habit Tracker: {e}")

        # به‌روزرسانی پیشرفت در کامیونیتی
        membership_request = get_object_or_404(MembershipRequest, community_id=community_id, requester=request.user, selected_habit=habit)

        # به‌روزرسانی selected_habit در درخواست عضویت
        membership_request.selected_habit.progress = habit.progress
        membership_request.selected_habit.save()

        return Response({'message': "Today's habit progress updated.", 'progress': habit.progress}, status=status.HTTP_200_OK)


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

    if not community_id or not selected_habit_id:
        return Response({"detail": "Both community_id and selected_habit_id are required."}, status=status.HTTP_400_BAD_REQUEST)

    community = get_object_or_404(Community, id=community_id)

    # # بررسی وجود درخواست عضویت مشابه فقط برای وضعیت‌های 'pending' و 'accepted'
    # if MembershipRequest.objects.filter(community=community, requester=requester, status__in=['pending', 'accepted']).exists():
    #     return Response({"detail": "Membership request already exists."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        selected_habit = Habit.objects.get(id=selected_habit_id)
    except Habit.DoesNotExist:
        return Response({"detail": "Selected habit does not exist."}, status=status.HTTP_400_BAD_REQUEST)

    membership_request = MembershipRequest.objects.create(
        community=community,
        requester=requester,
        selected_habit=selected_habit,
        status='pending'
    )

    return Response({
        "community_id": community_id,
        "selected_habit_id": selected_habit_id,
        "requester": requester.username,
        "status": membership_request.status
    }, status=status.HTTP_201_CREATED)


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

