from rest_framework import serializers
from .models import Community, Category , MembershipRequest
from HabitTracker.models import Habit
from django.contrib.auth.models import User # افزودن مدل User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields ='__all__'


class CommunitySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    habits = HabitSerializer(many=True)  # نمایش جزئیات هبیت‌ها

    habits = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), many=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    
    class Meta:
        model = Community
        fields =  ['id','user', 'title', 'description','categories','habits']  
        

    def validate_categories(self, value): 
        if len(value) != 1: 
            raise serializers.ValidationError("You must select exactly one category.") 
        return value

    def validate_habits(self, value): 
        if len(value) > 2: 
            raise serializers.ValidationError("You can select a maximum of 2 habits.") 
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
    requester_id = serializers.IntegerField(write_only=True, required=True)
    community = serializers.PrimaryKeyRelatedField(read_only=True) 
    requester = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = MembershipRequest
        fields = ['id', 'community', 'community_id', 'requester', 'requester_id', 'status', 'created_at']        
        read_only_fields = ['id', 'status', 'created_at']   

    

    def create(self, validated_data):
        community_id = validated_data.pop('community_id')
        requester_id = validated_data.pop('requester_id')
        try:
            community = Community.objects.get(id=community_id)
            requester = User.objects.get(id=requester_id)
        except Community.DoesNotExist:
            raise serializers.ValidationError({"community_id": "Community not found."})
        except User.DoesNotExist:
            raise serializers.ValidationError({"requester_id": "Requester not found."})
        
        if MembershipRequest.objects.filter(community=community, requester=requester).exists():
            raise serializers.ValidationError({"detail": "Membership request already exists."})

        membership_request = MembershipRequest.objects.create(community=community, requester=requester)
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
    
    
    