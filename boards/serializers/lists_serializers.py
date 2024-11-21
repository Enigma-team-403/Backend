# from rest_framework import serializers

# from cards.serializers import CardSerializer

# from ..models import List


# class ListSerializer(serializers.ModelSerializer):
#     cards = CardSerializer(many=True, read_only=True)

#     class Meta:
#         model = List
#         fields = '__all__'
#         read_only_fields = ['created_by', 'modified_at', 'modified_by', 'archived']



from rest_framework import serializers
from ..models import List

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'  # Include necessary fields, e.g., name, order
  



