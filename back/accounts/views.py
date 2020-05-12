from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from .serializers import UserCreationSerializer, UserNickNameSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes



# Create your views here.
user = get_user_model()


class User(ListView):
    @api_view(['POST'])
    @permission_classes((AllowAny, ))
    def sign_up(request):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            # print(serializer.data)
            return Response({'message' : '회원가입이 성공적으로 완료되었습니다.'})

