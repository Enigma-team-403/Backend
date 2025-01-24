from django.core.cache import cache
from rest_framework import serializers
from .models import Community, Category , MembershipRequest
from HabitTracker.models import Habit
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields ='__all__'    

class CommunityMemberSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(source='profile.profile_picture', read_only=True)
    selected_habit = serializers.SerializerMethodField()
    member_progress = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'profile_picture', 'selected_habit', 'member_progress']

    def get_selected_habit(self, obj):
        membership_request = MembershipRequest.objects.filter(requester=obj, community__members=obj).first()
        if membership_request and membership_request.selected_habit:
            return {
                'id': membership_request.selected_habit.id,
                'name': membership_request.selected_habit.name,
            }
        return None

    def get_member_progress(self, obj):
        selected_habit = self.get_selected_habit(obj)
        progress_data = []
        if selected_habit: 
            habit_id = selected_habit['id'] 
            progress_percentage = cache.get(f'habit_{habit_id}_progress', 0) 
            return { 'habit_id': habit_id, 
                    'habit_name': selected_habit['name'], 
                    'progress_percentage': progress_percentage, } 
        return None


class CommunitySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    habits = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), many=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    class Meta:
        model = Community
        fields =  ['id','user', 'title', 'description','categories','habits','members']  
        

    def validate_categories(self, value): 
        if len(value) > 2: 
            raise serializers.ValidationError("You can select a maximum of 2 categories.") 
        return value

    def validate_habits(self, value): 
        if len(value) != 1: 
            raise serializers.ValidationError("You must select exactly one habit.") 
        return value

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        members_data = validated_data.pop('members', [])
        habits_data = validated_data.pop('habits')
        community = Community.objects.create(**validated_data)
        community.members.set(members_data)
        community.categories.set(categories_data)
        community.habits.set(habits_data)
        return community

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories')
        habits_data = validated_data.pop('habits')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.create_time = validated_data.get('create_time', instance.create_time)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()

        instance.categories.set(categories_data)
        instance.habits.set(habits_data)
        return instance





class MembershipRequestSerializer(serializers.ModelSerializer):
    community_id = serializers.IntegerField(write_only=True, required=True)
    selected_habit_id = serializers.IntegerField(write_only=True, required=True)
    community = serializers.PrimaryKeyRelatedField(read_only=True)
    requester = serializers.PrimaryKeyRelatedField(read_only=True)
    selected_habit = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MembershipRequest
        fields = ['id', 'community', 'community_id', 'requester', 'status', 'created_at', 'selected_habit', 'selected_habit_id']
        read_only_fields = ['id', 'status', 'created_at']

    def create(self, validated_data):
        community_id = validated_data.pop('community_id')
        selected_habit_id = validated_data.pop('selected_habit_id')
        requester = self.context['request'].user
        
        try:
            community = Community.objects.get(id=community_id)
            selected_habit = Habit.objects.get(id=selected_habit_id)
        except Community.DoesNotExist:
            raise serializers.ValidationError({"community_id": "Community not found."})
        except Habit.DoesNotExist:
            raise serializers.ValidationError({"selected_habit_id": "Selected habit not found."})

        if MembershipRequest.objects.filter(community=community, requester=requester).exists():
            raise serializers.ValidationError({"detail": "Membership request already exists."})

        membership_request = MembershipRequest.objects.create(community=community, requester=requester, selected_habit=selected_habit)
        return membership_request

class ApproveMembershipRequestSerializer(serializers.Serializer): 
    request_id = serializers.IntegerField(required=True) 
    action = serializers.ChoiceField(choices=[('approve', 'Approve'), ('reject', 'Reject')])







class DetailsSerializer(serializers.ModelSerializer):
    habits = HabitSerializer(many=True, required=False) 
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=Category.objects.all())
    members = serializers.StringRelatedField(many=True) # نمایش اعضای فعلی به صورت لیست
    class Meta:
        model = Community
        fields = ['id', 'title', 'description', 'habits', 'categories', 'members']  
        


class AddMemberSerializer(serializers.Serializer): 
    user_id = serializers.IntegerField()
    
    
    