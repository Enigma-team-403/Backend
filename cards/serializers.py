
from rest_framework import serializers

from members.models import Member

from .models import Card


class CardSerializer(serializers.ModelSerializer):

    members = serializers.PrimaryKeyRelatedField(required=False, queryset=Member.objects.all(), many=True)

    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ['created_by', 'modified_at', 'modified_by', 'archived']
