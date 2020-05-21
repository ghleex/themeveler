from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser
from drf_yasg.utils import swagger_auto_schema
from decouple import config
from .serializers import MessageSerializer, MessageViewSerializer
from .models import Message, Theme

User = get_user_model()
decoder = api_settings.JWT_DECODE_HANDLER

# Create your views here.
def get_user(token, format=None):
    jwt_data = decoder(token[1])
    user = get_object_or_404(User, id=jwt_data['user_id'])
    return user


class TravelMgmt(APIView):
    """
    사용자의 여행 코스 관리

    ---
    """
    def get_person(self, user_pk, format=None):
        if User.objects.filter(pk=user_pk).exists():
            return User.objects.get(pk=user_pk)
        else:
            return None
    
    def get(self, request, user_pk, format=None):
        # try:
            user = self.get_person(user_pk)
            print(user)
            themes = user.favorite_themes
            dests = user.favorite_destinations
            data = {
                'message': 'ok',
                'favourite_themes': themes,
                'favourite_dests': dests,
            }
            return Response(data, status=status.HTTP_200_OK)
        # except:
        #     data = {
        #         'message': 'Error has occurred'
        #     }
        #     return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, pk, format=None):
        user = self.get_person(pk)
        # theme 을 어떻게 저장할지 생각해야 함
        pass


def map(request):
    KAKAO_API_KEY = config('KAKAO_API_KEY')
    context = {'KAKAO_API_KEY': KAKAO_API_KEY} 
    return render(request, 'travels/map.html', context)


@parser_classes((FormParser, ))
class Chating(APIView):
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


class AdminTravelMgmt(APIView):
    def add(self, theme, dests):
        
        pass

    def fetch(self, theme, ):
        # django form으로 직접 받아오는건 vue.js customizing이 너무 번거롭다.
        # 일반 form으로 받아온 뒤 django ORM 객체에 직접 넣으면서 validation 진행하는 방식으로 진행.
        pass
    
    # Theme의 ListTextField가 list 형태로 출력되는지 확인하기 위한 test 함수, list로 잘 출력됨

    # def test(request):
    #     theme = Theme.objects.get(id=1)
    #     print(type(theme.dests))
    #     for t in theme.dests:
    #         print(t)
    #     return Response()