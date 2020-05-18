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
    고객센터 - 사용자
    
    ---
    """
    def get_user(self, user_pk, format=None):
        try:
            if User.objects.filter(pk=user_pk).exists():
                return User.objects.get(pk=user_pk)
            else:
                raise Exception
        except:
            msg = {
                'message': 'NOT FOUND'
            }
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, user_pk, format=None):
        user = self.get_user(user_pk)
        serializer = CustomersVoiceSerializer(user)
        if user == request.data.get('request_user'):
            voices = Improvement.objects.get(request_user=user)
            data = {
                'voices': data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'voices': 'NONE',
                'message': 'INVALID ACCESS'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
            
    def post(self, request, user_pk, format=None):
        try:
            user = request.data.get['request_user']
            data = {
                'title': request.data.get['title'],
                'content': request.data.get['content'],
                'category': request.data.get['content'],
                'request_user': user,
                'manager': request.data.get['manager'],
                'message': ''
            }
            serializer = CustomersVoiceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                data['message'] = 'POSTING SUCCESS'
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(data, status=status.HTTP_204_NO_CONTENT)
        except:
            data = {
                'message': 'POSTING ERROR OCCURRED'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, user_pk, voice_pk, format=None):
        user = self.get_user(user_pk)
        voice = Improvement.objects.get(pk=voice_pk)



class ManagersReply(APIView):
    """
    고객센터 - 관리자
    
    ---
    """
    def get_manager(self, manager_pk, format=None):
        try:
            manager = User.objects.get(pk=manager_pk)
            if manager.is_staff:
                return manager
            else:
                raise Exception
        except:
            data = {
                'message': 'INVALID ACCESS'
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, manager_pk, format=None):
        manager = self.get_manager(manager_pk)
        todos = Improvement.objects.filter(manager=manager_pk)

    def post(self, request, manager_pk, format=None):
        manager = self.get_manager(manager_pk)

    def patch(self, request, manager_pk, todo_pk, format=None):
        manager = self.get_manager(manager_pk)
        todo = Improvement.objects.get(pk=todo_pk)
        title = request.data.get['title']
        content = request.data.get['content']
        category = request.data.get['category']
        data = {
            'title': title,
            'content': content,
            'category': category,
        }
        serializer = CustomersVoiceSerializer(data=data)

