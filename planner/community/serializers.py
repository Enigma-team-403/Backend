from rest_framework import serializers
<<<<<<< HEAD
from .models import Community, Category, Habit
=======
from .models import Community, Category , MembershipRequest
from HabitTracker.models import Habit
from django.contrib.auth.models import User # افزودن مدل User
>>>>>>> backendWithoutToken

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
<<<<<<< HEAD
        fields = ('id', 'name')
=======
        fields = '__all__'

>>>>>>> backendWithoutToken

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
<<<<<<< HEAD
        fields = ('id', 'name', 'description', 'user')

class CommunitySerializer(serializers.ModelSerializer):
    category_ids = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='categories', many=True)
    habit_ids = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), source='habits', many=True)

    class Meta:
        model = Community
        fields = ('id', 'title', 'description', 'create_time', 'category_ids', 'habit_ids', 'profile_picture')
=======
        fields ='__all__'


class CommunitySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    habits = HabitSerializer(many=True)  # نمایش جزئیات هبیت‌ها

    habits = serializers.PrimaryKeyRelatedField(queryset=Habit.objects.all(), many=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    
    class Meta:
        model = Community
        fields =  ['id','user', 'title', 'description','categories','habits']  
        
    # def create(self, validated_data):
    #     user = User.objects.first()  # تنظیم کاربر پیش‌فرض
    #     categories_data = validated_data.pop('categories', [])
    #     community = Community.objects.create(user=user, **validated_data)
    #     community.categories.set(categories_data)
    #     return community
>>>>>>> backendWithoutToken

    def validate_category_ids(self, value):
        if len(value) > 2:
            raise serializers.ValidationError("You can select a maximum of 2 categories.")
        return value

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
<<<<<<< HEAD
        habits_data = validated_data.pop('habits')
        community = Community.objects.create(**validated_data)
=======
        members_data = validated_data.pop('members', [])
        habits_data = validated_data.pop('habits')
        community = Community.objects.create(**validated_data)
        community.members.set(members_data)
>>>>>>> backendWithoutToken
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
<<<<<<< HEAD
        return instance
=======
        return instance
    
    


class MembershipRequestSerializer(serializers.ModelSerializer):
    community_id = serializers.IntegerField(write_only=True, required=True)
    requester_id = serializers.IntegerField(write_only=True, required=True)
    class Meta:
        model = MembershipRequest
        fields = ['id', 'community', 'community_id', 'requester', 'requester_id', 'status', 'created_at']        
        read_only_fields = ['id', 'status', 'created_at']   


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
    
    
    
>>>>>>> backendWithoutToken
