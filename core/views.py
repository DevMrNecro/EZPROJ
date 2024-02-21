from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser, File
from .serializers import UserSerializer, FileSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.http import FileResponse
from rest_framework.exceptions import PermissionDenied

# from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string

#signup
class UserSignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user_type = request.data.get('user_type')

        # Validate input
        if not (username and password and user_type) and not (email and password and user_type):
            return Response({'error': 'Please provide all required data'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'A user with the provided credentials already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        try:
            if email:
                user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
            else:
                user = CustomUser.objects.create_user(username=username, password=password, user_type=user_type)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Generate token
        token, _ = Token.objects.get_or_create(user=user)

        # Return response
        return Response({
            'user_id': user.id,
            'username': user.username,
            'user_type': user.user_type,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


#login
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate credentials
        if not (username and password):
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=username, password=password)
        print(user)

        if user:
            # User authenticated, generate token
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'user': str(user),'user_type':str(user.user_type), 'token': token.key}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'error': 'Unable to log in with provided credentials'}, status=status.HTTP_401_UNAUTHORIZED)

#FILE UPLOAD
class FileUploadView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type == 'OPS_USER':
            serializer.save(user=self.request.user)
        else:
            # If user is not OPS_USER, return a forbidden response
            raise PermissionDenied("You aren't allowed to perform this operation")

#DOWNLOAD FILE BY FILE ID
class FileDownloadView(generics.RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [AllowAny]

#VIEW ALL FILES
class FileListView(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [AllowAny]
