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
        ## 공통
            * categories: 전체 유형
        ## GET
            * category: 유형을 담을 리스트
        ## POST
            * category: 새롭게 만들 유형
    """
    def get(self, request, format=None):
        categories = VoiceCategory.objects.all()
        category = []
        for c in categories:
            serializer = VoiceCategorySerializer(c)
            category.append(serializer.data)
        if request.user.is_staff:
            data = {
                'data': category,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'data': '',
                'message': 'INVALID ACCESS',
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

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
        # 내용
            * category: 요청 유형 QuerySet
        
    """
    def get_category(self, category_pk, format=None):
        return get_object_or_404(VoiceCategory, pk=category_pk)
        
    def put(self, request, category_pk, format=None):
        category = self.get_category(category_pk)
        category.category = request.data.get('category')
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


class CustomersVoices(APIView):
    """
        고객센터(사용자) - 요청 글 조회/등록

        ---
        # 내용
            * voices: 해당 유저의 고객센터 작성 글 QuerySet
        ## GET
            * return 값: voice 목록(요청자와 실제 사용자가 같은 경우) / 부적절한 엑세스 메시지(요청자와 실제 사용자가 다른 경우)
    """
    def get(self, request, user_pk, format=None):
        request_user = request.user
        if user_pk == request_user.pk:
            voices = CustomersVoice.objects.filter(request_user=user_pk)
            voice = []
            for v in voices:
                serializer = CustomersVoiceSerializer(v)
                voice.append(serializer.data)
            data = {
                'voices': voice,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'voices': '',
                'message': 'INVALID ACCESS'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
            
    def post(self, request, user_pk, format=None):
        if user_pk == request.user.pk:
            user = request.user.username
            data = {
                'title': request.data.get('title'),
                'content': request.data.get('content'),
                'category': request.data.get('category'),
                'request_user': user,
                'manager': request.data.get('manager'),
            }
            serializer = CustomersVoiceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'title': '',
                'content': '',
                'category': '',
                'request_user': '',
                'manager': '',
                'message': 'INVALID ACCESS',
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class CustomersVoiceChange(APIView):
    """
        고객센터(사용자) - 요청 글 내용 수정
        
        ---
        # 내용
            * voice: 고객센터 내에서 사용자가 선택한 글
        ## PUT
            * return 값: voice.id
    """
    def get_user(self, user_pk, format=None):
        return get_object_or_404(User, pk=user_pk)
    
    def put(self, request, user_pk, voice_pk, format=None):
        if user_pk == request.user.pk:
            user = self.get_user(user_pk)
            voice = CustomersVoice.objects.get(pk=voice_pk)
            voice.title = request.data.get('title')
            voice.content = request.data.get('content')
            voice.category = VoiceCategory.objects.get(pk=request.data.get('category'))
            data = {
                'title': voice.title,
                'content': voice.content,
                'category': voice.category,
            }
            serializer = CustomersVoiceSerializer(voice, data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(voice.id, status=status.HTTP_200_OK)
        else:
            data = {
                'title': '',
                'content': '',
                'category': '',
                'message': 'INVALID ACCESS',
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)


class ManagersReplying(APIView):
    """
        고객센터(관리자) - 처리할 일 목록/등록

        ---
        # 내용
            * manager: 관리자
        ## GET
            * todos: 관리자가 처리할 글들
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
            'todos': todos,
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
        고객센터(관리자) - 관리자의 답변 수정
        
        ---
        # 내용
            * manager: 관리자
            * todo: 답변했던 글
    """
    def put(self, request, manager_pk, todo_pk, format=None):
        manager = get_object_or_404(User, pk=manager_pk)
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
