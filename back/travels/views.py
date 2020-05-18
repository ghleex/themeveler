from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from decouple import config
from .serializers import MessageSerializer
from .models import Message

User = get_user_model()
decoder = api_settings.JWT_DECODE_HANDLER

# Create your views here.
class TravelMgmt(APIView):
    """
    사용자의 여행 코스 관리

    ---
    """
    def get_person(self, user_id, format=None):
        if User.objects.filter(pk=user_id).exists():
            return User.objects.get(pk=user_id)
        else:
            return None
    
    def get(self, request, pk, format=None):
        # try:
            user = self.get_person(pk)
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


class Chating(APIView):
    def get(self, request, format=None):
        data = {}
        value = request.data.get('theme')
        if not value:
            data[form] = ['이 필드는 필수항목 입니다.']
            return Response(data)
        serializer = MessageSerializer(Message.objects.filter(theme=request.data.get('theme')), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
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