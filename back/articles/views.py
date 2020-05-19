from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import VoiceCategory, CustomersVoice, ManagersReply
from .serializers import VoiceCategorySerializer, CustomersVoiceSerializer, ManagerReplySerializer

User = get_user_model()
# Create your views here.
class SetVoiceCategory(APIView):
    """
    고객센터(관리자) - "요청 유형" 항목 조회/생성

    ---
    # 내용
        - categories: 전체 유형
        - category(GET): 유형을 담을 리스트
        - category(POST): 새롭게 만들 유형
    """
    def get(self, request, format=None):
        categories = VoiceCategory.objects.all()
        category = []
        for c in categories:
            serializer = VoiceCategorySerializer(c)
            category.append(serializer.data)
        # if User.is_staff():
        data = {
            'data': category,
        }
        return Response(data, status=status.HTTP_200_OK)
        # else:
        #     data = {
        #         'data': '',
        #         'message': 'INVALID ACCESS',
        #     }
        #     return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        category = request.data.get('category')
        data = {
            'category': category,
        }
        serializer = VoiceCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ChangeVoiceCategory(APIView):
    """
    고객센터(관리자) - "요청 유형" 항목 수정/삭제

    ---
    """
    def get_category(self, category_pk, format=None):
        return get_object_or_404(VoiceCategory, pk=category_pk)
        
    def put(self, request, category_pk, format=None):
        category = self.get_category(category_pk)
        category.category = request.data.get['category']
        data = {
            'category': category.category,
        }
        serializer = VoiceCategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(category.id, status=status.HTTP_200_OK)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_pk, format=None):
        category = self.get_category(category_pk)
        category.delete()
        msg = {
            'message': 'SUCCESSFULLY DELETED THE CATEGORY'
        }
        return Response(msg, status=status.HTTP_204_NO_CONTENT)


class CustomersVoice(APIView):
    """
    고객센터(사용자) - 요청 글 조회/등록

    ---

    """
    def get(self, request, user_pk, format=None):
        if User == request.data.get('request_user'):
            voices = CustomersVoice.objects.filter(request_user=User)
            data = {
                'voices': data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'voices': '',
                'message': 'INVALID ACCESS'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
            
    def post(self, request, user_pk, format=None):
        try:
            user = request.data.get['request_user']
            data = {
                'title': request.data.get['title'],
                'content': request.data.get['content'],
                'category': request.data.get['content'],
                'request_user': user,
                'manager': request.data.get['manager'],
            }
            serializer = CustomersVoiceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except:
            data = {
                'message': 'POSTING ERROR OCCURRED'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class CustomersVoiceChange(APIView):
    """
    고객센터(사용자) - 요청 글 내용 수정
    
    ---
    """
    def get_user(self, user_pk, format=None):
        return get_object_or_404(User, pk=user_pk)
    
    def put(self, request, user_pk, voice_pk, format=None):
        user = self.get_user(user_pk)
        voice = CustomersVoice.objects.get(pk=voice_pk)
        voice.title = request.data.get('title')
        voice.content = request.data.get('content')
        voice.category = request.data.get('category')
        data = {
            'title': voice.title,
            'content': voice.content,
            'category': voice.category,
        }
        serializer = CustomersVoiceSerializer(voice, data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(voice.id, status=status.HTTP_200_OK)


class ManagersReply(APIView):
    """
    고객센터(관리자): 처리할 일 목록/등록

    ---
    """
    def get_manager(self, manager_pk, format=None):
        try:
            manager = get_object_or_404(User, pk=manager_pk)
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
        todos = CustomersVoice.objects.filter(manager=manager_pk)
        data = {
            'todos': todos
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'is_fixed': True
        }
        serializer = ManagerReplySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ManagersReplyChange(APIView):
    """
    고객센터(관리자): 관리자의 답변 수정
    
    ---
    """
    def put(self, request, manager_pk, todo_pk, format=None):
        manager = get_object_or_404()
        todo = get_object_or_404(CustomersVoice, pk=todo_pk)
        todo.title = request.data.get['title']
        todo.content = request.data.get['content']
        data = {
            'title': todo.title,
            'content': todo.content,
        }
        serializer = CustomersVoiceSerializer(todo, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(todo.id, status=status.HTTP_200_OK)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
