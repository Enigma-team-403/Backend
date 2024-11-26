
# from rest_framework import serializers

# from ..models import Board
# from .lists_serializers import ListSerializer

# class BoardSerializer(serializers.ModelSerializer):
#     lists = ListSerializer(many=True, read_only=True)

#     class Meta:
#         model = Board
#         fields = '__all__'
#         read_only_fields = ['created_by', 'modified_at', 'modified_by', 'archived']



from rest_framework import serializers
from boards.models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'  # Include all fields that you want to expose (e.g., name, created_by, etc.)
        read_only_fields = ['created_at', 'modified_at']  # Make fields like timestamps read-only

    def create(self, validated_data):
        # Automatically set 'created_by' to the logged-in user (useful if you're handling authentication)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)
