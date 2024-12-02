from django.shortcuts import render
from members.serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth import get_user_model
from .utils import generate_access_token
import jwt


from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import CustomRefreshToken

from rest_framework import generics



from rest_framework import permissions, status


from rest_framework_simplejwt.tokens import RefreshToken
from members.models import User


class CustomTokenObtainPairView(TokenObtainPairView):
    token_class = CustomRefreshToken








class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # You can fetch user-related data here
        tokens = {
            'access': str(RefreshToken.for_user(user).access_token),
            'refresh': str(RefreshToken.for_user(user)),
        }
        return Response({'user': user.username, 'tokens': tokens}, status=status.HTTP_200_OK)
	



def get_logged_in_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    logged_in_users = [session.get_decoded().get('_auth_user_id') for session in active_sessions]
    return logged_in_users




class LoggedInUsersView(APIView):
    def get(self, request):
        logged_in_users = [user.username for user in User.objects.all() if user.is_authenticated]
        return Response({"logged_in_users": logged_in_users})



class UserRegistrationAPIView(APIView):
	serializer_class = UserRegistrationSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)

	def get(self, request):
		content = { 'message': 'Hello!' }
		return Response(content)

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception=True):
			new_user = serializer.save()
			if new_user:
				access_token = generate_access_token(new_user)
				data = { 'access_token': access_token }
				response = Response(data, status=status.HTTP_201_CREATED)
				response.set_cookie(key='access_token', value=access_token, httponly=True)
				return response
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserLogoutAPIView(APIView):
    def post(self, request):
        # Get the refresh token from the request
        refresh_token = request.data.get("refresh_token")

        # Find the token in the database
        token = Token.objects.filter(refresh_token=refresh_token).first()

        if token:
            # Mark the token as expired
            token.expired = True
            token.save()

            return Response({"message": "Logout successful"})
        else:
            return Response({"detail": "Token not found"}, status=status.HTTP_404_NOT_FOUND)



class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)

	def post(self, request):
		email = request.data.get('email', None)
		user_password = request.data.get('password', None)

		if not user_password:
			raise AuthenticationFailed('A user password is needed.')

		if not email:
			raise AuthenticationFailed('An user email is needed.')

		user_instance = authenticate(username=email, password=user_password)

		if not user_instance:
			raise AuthenticationFailed('User not found.')

		if user_instance.is_active:
			user_access_token = generate_access_token(user_instance)
			response = Response()
			response.set_cookie(key='access_token', value=user_access_token, httponly=True)
			response.data = {
				'access_token': user_access_token
			}
			return response

		return Response({
			'message': 'Something went wrong.'
		})



class UserViewAPI(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)

	def get(self, request):
		user_token = request.COOKIES.get('access_token')

		if not user_token:
			raise AuthenticationFailed('Unauthenticated user.')

		payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

		user_model = get_user_model()
		user = user_model.objects.filter(user_id=payload['user_id']).first()
		user_serializer = UserRegistrationSerializer(user)
		return Response(user_serializer.data)



class UserLogoutViewAPI(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (AllowAny,)

	def get(self, request):
		user_token = request.COOKIES.get('access_token', None)
		if user_token:
			response = Response()
			response.delete_cookie('access_token')
			response.data = {
				'message': 'Logged out successfully.'
			}
			return response
		response = Response()
		response.data = {
			'message': 'User is already logged out.'
		}
		return response


from rest_framework import viewsets

from .models import Member
from .serializers import MemberSerializer


class MemberViewSet(viewsets.ModelViewSet):
    """
    ViewSet to provide CRUD functionality for Member models
    """
    serializer_class = MemberSerializer

    def get_queryset(self):
        """
        Can be adjusted to filter for specific members
        :return: QuerySet
        """
        return Member.objects.all()



