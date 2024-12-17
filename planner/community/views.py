<<<<<<< HEAD
from urllib import response
from rest_framework import viewsets, permissions
from .models import Community, Category, Habit
from .serializers import CommunitySerializer, CategorySerializer, HabitSerializer
from rest_framework.response import Response
from rest_framework import status


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Community.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'community': serializer.data,
            'communities': CommunitySerializer(self.get_queryset(), many=True).data
        }, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

=======
from requests import Response
from rest_framework import viewsets, permissions
from .models import Community, Category ,MembershipRequest
from .serializers import CommunitySerializer, DetailsSerializer, HabitSerializer,MembershipRequestSerializer, ApproveMembershipRequestSerializer,AddMemberSerializer,CategorySerializer
from HabitTracker.models import Habit
from rest_framework.decorators import action , api_view
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


>>>>>>> backendWithoutToken
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

<<<<<<< HEAD
class UserHabitViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(habits, many=True)
        return response(serializer.data)
=======
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
    # permission_classes = [IsAuthenticated] 
    
    filter_backends = [DjangoFilterBackend] 
    filterset_class = CommunityFilter
    search_fields = ['title']
    filterset_fields = ['category']



    def perform_create(self, serializer):
        # user = User.objects.first()  # در اینجا می‌توانید کاربر پیش‌فرض را تنظیم کنید
        # if not Habit.objects.filter(user=user).exists():
        #     raise serializer.ValidationError({"detail": "You need to create at least one habit before creating a community."})
        # serializer.save(user=user)  # ذخیره کامیونیتی با تنظیم کاربر سازنده
        serializer.save(user=self.request.user)  # اینجا کاربر را تنظیم می‌کنیم

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
                    user = None             
        if user and not Habit.objects.filter(user=user).exists():
            return Response({"error": "No habits found for this user."}, status=400)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    
    def list(self, request, *args, **kwargs):
        communities = self.get_queryset()
        serializer = CommunitySerializer(communities, many=True)
        
        for community in serializer.data:
            community['compage_url'] = f"/compage/community/{community['id']}/"

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
        community = self.get_object()
        serializer = self.get_serializer(community, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        community = self.get_object()
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_habits(self, request, pk=None):
        community = self.get_object() 
        user = request.user  # گرفتن کاربر فعلی

        user_habits = Habit.objects.filter(user=user)
        
        if not user_habits.exists():
            create_habit = request.data.get('create_habit', None)
            if create_habit is None:
                return Response(
                    {"detail": "You need to create at least one habit before adding to a community. Do you want to create a habit?"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if create_habit.lower() == "yes":
                habit_name = request.data.get('habit_name', None)
                if not habit_name:
                    return Response(
                        {"detail": "Please provide a name for your new habit."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                new_habit = Habit.objects.create(user=user, name=habit_name, description="Your new habit", duration=30, goal=10)
                user_habits = Habit.objects.filter(user=user)  # به‌روزرسانی لیست هبیت‌های کاربر
                return Response(
                    {"detail": f"New habit '{habit_name}' created. You can now add it to the community."},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"detail": "You need to create at least one habit before adding to a community."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if community.external_habits.count() >= 2:
            return Response(
                {"detail": "You can add a maximum of 2 habits to the community."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        habit_ids = request.data.get('habit_ids', [])
        
        habits_to_add = Habit.objects.filter(id__in=habit_ids, user=user)
        if habits_to_add.count() != len(habit_ids):
            return Response(
                {"detail": "You can only add your own habits."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        community.external_habits.add(*habits_to_add)
        
        serializer = HabitSerializer(community.external_habits.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

    #============ SHADI's codes ===============

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
        # elif request.method == 'POST':
        #     return Response({"detail": "POST method is not implemented for this endpoint."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['get', 'post'])
    def add_members(self, request, pk=None):
        community = self.get_object()
        # if request.user != community.user:
        #     return Response({"detail": "Only the creator can add members."}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'POST':
            serializer = AddMemberSerializer(data=request.data)
            if serializer.is_valid():
                user_id = serializer.validated_data['user_id']
                try:
                    user = User.objects.get(id=user_id)
                    community.members.add(user)
                    return Response({"detail": "Member added successfully."}, status=status.HTTP_201_CREATED)
                except User.DoesNotExist:
                    return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # نمایش فرم HTML برای متد GET
        html_form = '''
            <html>
            <head>
                <title>Add Members</title>
            </head>
            <body>
                <h1>Add Members</h1>
                <form method="post">
                    <label for="user_id">User ID:</label><br>
                    <input type="number" id="user_id" name="user_id" required><br><br>
                    <button type="submit">Add Member</button>
                </form>
            </body>
            </html>
        '''
        return HttpResponse(html_form)

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

        # تشخیص سازنده‌ی کامیونیتی بدون نیاز به احراز هویت
        if community.user and community.user != user:
            return Response({"detail": "Only the community admin can accept membership requests."}, status=status.HTTP_403_FORBIDDEN)

        try:
            membership_request = MembershipRequest.objects.get(id=request_id, community=community)
            membership_request.status = 'accepted'
            membership_request.save()

            community.members.add(membership_request.requester)
            return Response({"detail": "Membership request accepted and user added to community."}, status=status.HTTP_200_OK)
        except MembershipRequest.DoesNotExist:
            return Response({"detail": "Membership request not found."}, status=status.HTTP_404_NOT_FOUND)

class UserHabitViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]

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
    # permission_classes = [permissions.IsAuthenticated]

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



@api_view(['GET', 'POST'])
def send_membership_request(request):
    if request.method == 'POST':
        community_id = request.data.get('community_id')
        requester_id = request.data.get('requester_id')
        serializer = MembershipRequestSerializer(data={'community_id': community_id, 'requester_id': requester_id})

        if serializer.is_valid():
            community_id = serializer.validated_data['community_id']
            requester_id = serializer.validated_data['requester_id']
            try:
                community = Community.objects.get(id=community_id)
                requester = User.objects.get(id=requester_id)
                if MembershipRequest.objects.filter(community=community, requester=requester).exists():
                    return Response({"detail": "Membership request already exists."}, status=status.HTTP_400_BAD_REQUEST)
                membership_request = MembershipRequest.objects.create(community=community, requester=requester)
                response_serializer = MembershipRequestSerializer(membership_request)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except Community.DoesNotExist:
                return Response({"detail": "Community not found."}, status=status.HTTP_404_NOT_FOUND)
            except User.DoesNotExist:
                return Response({"detail": "Requester not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # نمایش فرم HTML برای متد GET
    html_form = '''
        <html>
        <head>
            <title>Send Membership Request</title>
        </head>
        <body>
            <h1>Send Membership Request</h1>
            <form method="post">
                <label for="community_id">Community ID:</label><br>
                <input type="number" id="community_id" name="community_id" required><br>
                <label for="requester_id">Requester ID:</label><br>
                <input type="number" id="requester_id" name="requester_id" required><br><br>
                <button type="submit">Send Request</button>
            </form>
        </body>
        </html>
    '''
    return HttpResponse(html_form)



@api_view(['GET', 'POST'])
def view_membership_requests(request, community_id):
    if request.method == 'POST':
        try:
            community = Community.objects.get(id=community_id)
            membership_requests = MembershipRequest.objects.filter(community=community)
            serializer = MembershipRequestSerializer(membership_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Community.DoesNotExist:
            return Response({"detail": "Community not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # نمایش فرم HTML برای متد GET
    html_form = '''
        <html>
        <head>
            <title>View Membership Requests</title>
        </head>
        <body>
            <h1>View Membership Requests</h1>
            <form method="post">
                <label for="community_id">Community ID:</label><br>
                <input type="number" id="community_id" name="community_id" value="{}" readonly><br><br>
                <button type="submit">View Requests</button>
            </form>
        </body>
        </html>
    '''.format(community_id)
    return HttpResponse(html_form)

@api_view(['GET', 'POST'])
def manage_membership_request(request, community_id):
    if request.method == 'POST':
        serializer = ApproveMembershipRequestSerializer(data=request.data)
        if serializer.is_valid():
            request_id = serializer.validated_data['request_id']
            action = serializer.validated_data['action']

            try:
                community = Community.objects.get(id=community_id)
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
    
    # نمایش فرم HTML برای متد GET
    html_form = '''
        <html>
        <head>
            <title>Manage Membership Request</title>
        </head>
        <body>
            <h1>Manage Membership Request</h1>
            <form method="post">
                <label for="request_id">Request ID:</label><br>
                <input type="number" id="request_id" name="request_id" required><br>
                <label for="action">Action:</label><br>
                <select id="action" name="action" required>
                    <option value="approve">Approve</option>
                    <option value="reject">Reject</option>
                </select><br><br>
                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
    '''
    return HttpResponse(html_form)
>>>>>>> backendWithoutToken
