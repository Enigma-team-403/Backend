from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserRegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
	class Meta:
		model = get_user_model()
		fields = ['email', 'username', 'password']

	def create(self, validated_data):
		user_password = validated_data.get('password', None)
		db_instance = self.Meta.model(email=validated_data.get('email'), username=validated_data.get('username'))
		db_instance.set_password(user_password)
		db_instance.save()
		return db_instance



class UserLoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=100)
	username = serializers.CharField(max_length=100, read_only=True)
	password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
	token = serializers.CharField(max_length=255, read_only=True)



# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})

#     class Meta:
#         model = get_user_model()
#         fields = ['email', 'username', 'password']

#     def validate_email(self, value):
#         if get_user_model().objects.filter(email=value).exists():
#             raise serializers.ValidationError("Email is already in use.")
#         return value

#     def validate_username(self, value):
#         if get_user_model().objects.filter(username=value).exists():
#             raise serializers.ValidationError("Username is already in use.")
#         return value

#     def create(self, validated_data):
#         user_password = validated_data.get('password', None)
#         db_instance = self.Meta.model(email=validated_data.get('email'), username=validated_data.get('username'))
#         db_instance.set_password(user_password)
#         db_instance.save()
#         return db_instance


# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=100)
#     username = serializers.CharField(max_length=100, read_only=True)
#     password = serializers.CharField(max_length=100, min_length=8, style={'input_type': 'password'})
#     token = serializers.CharField(max_length=255, read_only=True)
