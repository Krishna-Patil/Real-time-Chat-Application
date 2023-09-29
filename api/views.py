from django.contrib.auth import login, authenticate

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from .utils import suggest_friends
from users.models import CustomUser


class RegistrationAPIView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class OnlineUsersAPIView(generics.ListAPIView):
    """
    returns a list of users who are online
    """

    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.filter(is_online=True)
    serializer_class = CustomUserSerializer


class LoginAPIView(APIView):
    """
    logs user into the platform and sets its status to online
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data["username"]
        password = serializer.data["password"]
        user = authenticate(username=username, password=password)
        try:
            login(request, user)
            request.user.is_online = True
            refresh = RefreshToken.for_user(request.user)

            response = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Internal server error!", status=status.HTTP_404_NOT_FOUND)


class StartChatAPIView(APIView):
    """
    Allows a user to initiate a chat with another user who is online and available
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = StartChatSerializer

    def post(self, request):
        serializer = StartChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data["username"]
        usr = CustomUser.objects.get(username=username)
        if usr.is_online == True:
            return Response(
                "User is online and available to chat!", status=status.HTTP_200_OK
            )
        return Response(
            "User is not online and not available to chat!",
            status=status.HTTP_400_BAD_REQUEST,
        )


class SuggestFriendsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            json_data = suggest_friends(user_id)
            return Response(json_data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                "Internal server error!", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
