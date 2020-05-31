from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import permission_classes, parser_classes
from rest_framework.parsers import FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from decouple import config
from .serializers import MessageSerializer, MessageViewSerializer, ThemeSerializer, DestinationSerializer
from .models import Message, Theme, Destination
from accounts.serializers import UserNicknameSerializer

User = get_user_model()
decoder = api_settings.JWT_DECODE_HANDLER

not_valid_message = {
    'message': 'THE SERIALIZER IS NOT VALID'
}
error_message = {
    'message': 'AN ERROR HAS BEEN OCCURRED'
}

# Create your views here.
def map(request):
    KAKAO_API_KEY = config('KAKAO_API_KEY')
    context = {'KAKAO_API_KEY': KAKAO_API_KEY} 
    return render(request, 'travels/map.html', context)


def get_user(token, format=None):
    # JWT 통하여 유저 확인하기 위한 범용 함수
    jwt_data = decoder(token[1])
    user = get_object_or_404(User, id=jwt_data['user_id'])
    return user


@permission_classes((IsAuthenticated,))
class VisitedThemes(APIView):
    """
        사용자의 여행 코스 관리

        ---
        # 내용
            * 방문했던 코스(테마) 목록 열람, 추가/삭제
    """
    def get(self, request, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        try:
            themes = user.visited_themes.all()
            theme = [ThemeSerializer(t).data for t in themes] 
            fav_themes = user.favorite_themes.all()
            fav_theme = [ThemeSerializer(ft).data for ft in fav_themes]

            data = {
                'message': 'ok',
                'visited_themes': theme,
                'favorite_themes': fav_theme,
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        try:            
            themes = user.visited_themes.all()
            req_themes = request.data.get('visited_themes').split(', ')
            message = {
                'message': '',
            }
            for rt in req_themes:
                if themes.filter(pk=rt).exists():
                    user.visited_themes.remove(rt)
                    message['message'] = f'{user} is removed from visited'
                else:
                    user.visited_themes.add(rt)
                    message['message'] = f'{user} is added to visited'
            else:
                return Response(message, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class VisitedDest(APIView):
    """
        사용자가 방문한 장소 목록/추가
        
        ---
    """    
    def get(self, request, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        try:
            dests = user.dests.all()
            dest = [DestinationSerializer(d).data for d in dests]            
            fav_dests = user.favorite_destinations.all()
            fav_dest = [DestinationSerializer(fd).data for fd in fav_dests]

            data = {                
                'visited_dests': dest,
                'favorite_dests': fav_dest,
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        try:
            dests = user.dests.all()
            req_dests = request.data.get('visited_dests').split(', ')
            message = {
                'message': '',
            }
            for rd in req_dests:
                if dests.filter(pk=rd).exists():
                    user.dests.remove(rd)
                    message['message'] = f'{user.username} is removed from visitors'
                else:
                    user.dests.add(rd)
                    message['message'] = f'{user.username} is added to visitors'
                return Response(message, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


# @permission_classes((IsAuthenticated,))
class Like(APIView):
    """
        사용자의 테마 좋아요/취소
        
        ---
    """
    def get_theme(self, theme_pk, format=None):
        return get_object_or_404(Theme, pk=theme_pk)

    def get(self, request, theme_pk, format=None):
        theme = self.get_theme(theme_pk)
        try:
            likes = theme.theme_like_users.all()
            users = [UserNicknameSerializer(l).data for l in likes]
            data = {
                'like_users_count': theme.theme_like_users.count(),
                'like_users': users,
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, theme_pk, format=None):
        theme = self.get_theme(theme_pk)
        user =  get_user(request.headers['Authorization'].split(' '))
        try:
            message = {
                'message': '',
                'add_or_remove': 0
            }
            if theme.theme_like_users.filter(pk=user.pk).exists():
                theme.theme_like_users.remove(user)
                message['message'] = f'{user.username} is removed from like_users'
            else:
                theme.theme_like_users.add(user)
                message['message'] = f'{user.username} added to like_users'
                message['add_or_remove'] = 1
            return Response(message, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


class Chatting(APIView):
    @swagger_auto_schema(query_serializer=MessageViewSerializer)
    def get(self, request, theme_pk, format=None):
        """
            채팅 내역 확인(테마) - 테마별 채팅 내역을 확인합니다.

            # 내용
                * headers에서 포함된 jwt 데이터의 user_id를 이용합니다.
                * theme_pk: theme의 theme_id를 작성합니다. Int 형식입니다.
        """
        data = {}
        theme = request.GET.get('theme')
        serializer = MessageSerializer(Message.objects.filter(theme=theme_pk), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(query_serializer=MessageSerializer)
    def post(self, request, theme_pk, format=None):
        """
            채팅 저장(테마) - 테마별 채팅을 저장합니다..

            # 내용
                * headers에서 포함된 jwt 데이터의 user_id를 이용합니다.
                * theme_pk: theme의 theme_id를 작성합니다. Int 형식입니다.
                * message: 메시지를 작성합니다.
        """
        jwt_data = decoder(request.headers['Authorization'].split(' ')[1])
        user = User.objects.get(id=jwt_data.get('user_id'))
        data = {
            'theme': theme_pk,
            'nickname': user.anonymous,
            'message': request.data.get('message')
        }
        serializer = MessageSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class AllTheme(APIView):
    def get(self, request):
        all_theme = Theme.objects.all()
        if not all_theme:
            return Response('Theme is not existed', status=status.HTTP_400_BAD_REQUEST)
        serialized_all_theme = [ThemeSerializer(theme).data for theme in all_theme]
        data = {
            'all_theme' : serialized_all_theme
        }
        return Response(data)

class Destinations(APIView):
    def get(self, request, theme_pk):
        destinations = []
        theme = get_object_or_404(Theme, pk=theme_pk)
        for dest_pk in theme.dests:
            destination = Destination.objects.filter(pk=dest_pk)[0]
            if destination:
                destinations.append(DestinationSerializer(destination).data)
            else:
                return Response('Destination is not exist', status=status.HTTP_400_BAD_REQUEST)

        user = get_user(request.headers['Authorization'].split(' '))
        is_like = False
        if theme.theme_like_users.filter(pk=user.pk).exists():
            is_like = True
        data = {
            'destinations' : destinations,
            'like_count': theme.theme_like_users.count(),
            'is_like': is_like
        }
        return Response(data) if destinations else Response(error_message, status=status.HTTP_400_BAD_REQUEST)

class FilteredTheme(APIView):
    def get(self, request, region):
        filtered_theme = ThemeSerializer(Theme.objects.filter(region=region)) if region else ThemeSerializer(Theme.objects.all())
        if not filtered_theme:
            return Response('Theme is not existed', status=status.HTTP_400_BAD_REQUEST)
        
        return filtered_theme


            
    
