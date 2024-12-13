from requests import Response
from rest_framework import viewsets, permissions
from .models import Community, Category, Habit
from .serializers import CommunitySerializer, CategorySerializer, HabitSerializer
from HabitTracker.models import Habit
from rest_framework.decorators import action
from rest_framework.response import Response
from HabitTracker.models import Habit
from HabitTracker.serializers import HabitSerializer
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, CharFilter        
from django.shortcuts import render


def community_list_view(request):
    communities = Community.objects.all()

    name_query = request.GET.get('name', '')
    if name_query:
        communities = communities.filter(name__icontains=name_query)

    category_query = request.GET.get('category', '')
    if category_query:
        communities = communities.filter(category__name__icontains=category_query)

    return render(request, 'community/community_list.html', {'communities': communities})

class CommunityFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Community Name')
    category = CharFilter(field_name='category__name', lookup_expr='icontains', label='Category Name')

    class Meta:
        model = Community
        fields = ['name', 'category']

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = CommunityFilter
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def community_list_view(request):
        communities = Community.objects.all()

        name_query = request.GET.get('name', '')
        if name_query:
            communities = communities.filter(name__icontains=name_query)

        category_query = request.GET.get('category', '')
        if category_query:
            communities = communities.filter(category__name__icontains=category_query)

        return render(request, 'community/community_list.html', {'communities': communities})

    def create(self, request, *args, **kwargs):
        user = request.user

        if not Habit.objects.filter(user=user).exists():
            return Response(
                {"detail": "You need to create at least one habit before creating a community."},
                status= status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

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
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        community = self.get_object()  # پیدا کردن کامیونیتی از طریق id
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
    

        
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserHabitViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data)


