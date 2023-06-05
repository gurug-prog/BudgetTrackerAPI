from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserProfileSerializer
from . import services


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for registering, logging in and managing user profile.
    """

    # Register User
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = services.create_user(serializer.validated_data)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Login User
    @action(detail=False, methods=['post'])
    def login(self, request):
        user = services.authenticate_user(
            request.data.get('email'), request.data.get('password'))
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # Get User Profile
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        profile = services.get_user_profile(request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    # Update User Profile
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        profile = services.update_user_profile(request.user, request.data)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
