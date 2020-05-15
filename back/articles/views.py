from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Improvement
from .serializers import CustomersVoiceSerializer

User = get_user_model()
# Create your views here.
class CustomersVoice(APIView):
    """
    고객센터
    
    ---
    """
    def get_user(self, user_pk, format=None):
        if User.objects.filter(pk=user_pk).exists():
            return User.objects.get(pk=user_pk)
        else:
            msg = {
                'message': '존재하지 않는 사용자입니다.'
            }
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = CustomersVoiceSerializer(user)
        if user == request.data.get('username'):
            pass
            
    def post(self, request, pk, format=None):
        user = self.get_user(pk)
        title = request.data.get('title')
        content = request.data.get('content')
        category = request.data.get('category')
