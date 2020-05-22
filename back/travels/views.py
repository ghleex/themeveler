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
            dests = user.dests.all()
            theme, dest = [], []
            fav_themes = user.favorite_themes.all()
            fav_dests = user.favorite_destinations.all()
            fav_theme, fav_dest = [], []

            for t in themes:
                serializer_t = ThemeSerializer(t)
                print('t', serializer_t.data)
                theme.append(serializer_t.data)
            for d in dests:
                serializer_d = DestinationSerializer(d)
                print('d', serializer_d.data)
                dest.append(serializer_d.data)
            for ft in fav_themes:
                serializer_ft = ThemeSerializer(ft)
                fav_theme.append(serializer_ft.data)
            for fd in fav_dests:
                serializer_fd = DestinationSerializer(fd)
                fav_dest.append(serializer_fd.data)

            data = {
                'message': 'ok',
                'visited_themes': theme,
                'visited_dests': dest,
                'favorite_themes': fav_theme,
                'favorite_dests': fav_dest,
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
            user = get_user(request.headers['Authorization'].split(' '))
        # try:
            req_themes = request.data.get('visited_themes')
            req_dests = request.data.get('visited_dests')
            theme, dest = [], []
            for rt in req_themes:
                thm = Theme.objects.get(pk=rt)
                serializer_rt = ThemeSerializer(thm)
                theme.append(serializer_rt.data)
            for rd in req_dests:
                dst = Destination.objects.get(pk=rd)
                serializer_rd = DestinationSerializer(dst)
                dest.append(serializer_rd.data)
                
            message = {
                'message': '',
            }
            if user in theme:
                User.visited_themes.remove(user)
                message['message'] = f'{user} is removed from visited'
            else:
                User.visited_themes.add(user)
                message['message'] = f'{user} is added to visited'
            return Response(message, status=status.HTTP_200_OK)
        # except:
        #     return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class VisitedDest(APIView):
    """
        사용자가 방문한 장소 목록/추가
        
        ---
    """    
    def get(self, request, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        try:
            data = {
                'visitors': user.dests.all(),
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        message = {
            'message': '',
        }
        try:
            if Destination.visitors.filter(pk=user.pk).exists():
                Destination.visitors.remove(user)
                message['message'] = f'{user.username} is removed from visitors'
            else:
                Destination.visitors.add(user)
                message['message'] = f'{user.username} is added to visitors'
            return Response(message, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
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
            data = {
                'like_users': theme.theme_like_users.count()
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
            }
            if theme.theme_like_users.filter(pk=user.pk).exists():
                theme.theme_like_users.remove(user)
                message['message'] = f'{user.username} is removed from like_users'
            else:
                theme.theme_like_users.add(user)
                message['message'] = f'{user.username} added to like_users'
            return Response(message, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@parser_classes((FormParser, ))
class Chatting(APIView):
    @swagger_auto_schema(query_serializer=MessageViewSerializer)
    def get(self, request, format=None):
        """
            채팅 내역 확인(테마) - 테마별 채팅 내역을 확인합니다.

            # 내용
                * headers에서 포함된 jwt 데이터의 user_id를 이용합니다.
                * theme: theme의 theme_id를 작성합니다. Int 형식입니다.
        """
        data = {}
        theme = request.GET.get('theme')
        if not theme:
            data[theme] = ['이 필드는 필수항목 입니다.']
            return Response(data)
        serializer = MessageSerializer(Message.objects.filter(theme=theme), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(query_serializer=MessageSerializer)
    def post(self, request, format=None):
        """
            채팅 저장(테마) - 테마별 채팅을 저장합니다..

            # 내용
                * headers에서 포함된 jwt 데이터의 user_id를 이용합니다.
                * theme: theme의 theme_id를 작성합니다. Int 형식입니다.
                * message: 메시지를 작성합니다.
        """
        jwt_data = decoder(request.headers['Authorization'].split(' ')[1])
        user = User.objects.get(id=jwt_data.get('user_id'))
        data = {
            'theme' : request.data.get('theme'),
            'nickname' : user.anonymous,
            'message' : request.data.get('message')
        }
        serializer = MessageSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
