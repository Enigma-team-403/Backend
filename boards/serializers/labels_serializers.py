
# from rest_framework import serializers

# from ..models import Label


# class LabelSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Label
#         fields = '__all__'
#         read_only_fields = ['created_by', 'modified_at', 'modified_by', 'archived']


from rest_framework import serializers
from ..models import Label

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'  # Include necessary fields like text, board, etc.
