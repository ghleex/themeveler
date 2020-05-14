from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from decouple import config

User = get_user_model()
# Create your views here.
class TravelMgmt(APIView):
    def get_person(self, pk, format=None):
        if User.objects.filter(pk=pk).exists():
            return User.objects.get(pk=pk)
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


def map(request):
    KAKAO_API_KEY = config('KAKAO_API_KEY')
    context = {'KAKAO_API_KEY': KAKAO_API_KEY} 
    return render(request, 'travels/map.html', context)