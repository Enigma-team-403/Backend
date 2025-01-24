from rest_framework import serializers
from .models import Interest, UserInterest

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name', 'category']


class UserInterestSerializer(serializers.ModelSerializer):
    interest_name = serializers.CharField(source='interest.name', read_only=True)
    interest_category = serializers.CharField(source='interest.category', read_only=True)

    class Meta:
        model = UserInterest
        fields = ['id', 'interest', 'interest_name', 'interest_category']
