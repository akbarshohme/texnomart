from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from texnomart.serializers import LoginSerializer, RegisterSerializer

class LoginAPIView(APIView):
    def post(self, request,):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                'username': {
                    'detail': "User does not exist"
                }
            }
            username = serializer.data['username']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                token, created = Token.objects.get_or_create(user=user)
                response = {
                    'Success': True,
                    'Token': token.key,
                    'username': user.username,
                    'email': user.email,
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request,):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({
            'Success': True,
            'message': 'Successfully logged out.'
        }, status=status.HTTP_204_NO_CONTENT)


class RegisterAPIView(APIView):
    def post(self, request, ):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            token = Token.objects.get(user=user)
            return Response({
                'Success': True,
                'username': serializer.data['username'],
                'message': 'Successfully registered.',
                'Token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
