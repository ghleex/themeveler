from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler
from .serializers import UserCreationSerializer, UserNicknameSerializer, WaitingSerializer
from .serializers  import UsernameSerializer, ConfirmCodeSerializer, UserPasswordSerializer
from .models import Waiting
from random import SystemRandom
from datetime import datetime, timedelta, timezone
import re

# Create your views here.
User = get_user_model()
decoder = api_settings.JWT_DECODE_HANDLER

@permission_classes((AllowAny, ))
class Mail(APIView):
    def get(self, request, format=None):
        check_forms = ['username', 'confirm_code']
        data = {}
        for form in check_forms:
            value = request.data.get(form)
            if not value:
                data[form] = ['이 필드는 필수항목 입니다.']
            elif form == 'username':
                p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
                if p.match(value) == None:
                    data[form] = ['email형식이 아닙니다.']

        if data:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if Waiting.objects.filter(username=request.data.get('username')).exists():
            waiting_user = Waiting.objects.get(username=request.data.get('username'))
            if waiting_user.is_confirm:
                return Response({'message' : ['이미 인증된 유저입니다.']})
            if waiting_user.username == request.data.get('username') and waiting_user.confirm_code == request.data.get('confirm_code'):
                if waiting_user.updated_at > datetime.now(timezone.utc) - timedelta(minutes=10):
                    waiting_user.is_confirm = True
                    waiting_user.confirm_code = None
                    waiting_user.save()
                    return Response({'message' : ['메일 인증 성공.']})
                else:
                    return Response({'message' : ['유효시간이 지났습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message' : ['인증에 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        if UsernameSerializer(data=request.data).is_valid(raise_exception=True):
            confirm_code = ''
            username = request.data.get('username')
            for cnt in range(3):
                sr = SystemRandom()
                confirm_code += str(sr.choice(range(1000, 10000)))
                if cnt != 2:
                    confirm_code += '-'
            data = {
                'username' : username,
                'confirm_code': confirm_code
            }
            print(Waiting.objects.filter(username=username).exists())
            if Waiting.objects.filter(username=username).exists():
                waiting_user = Waiting.objects.get(username=username)
                print()
                print(waiting_user)
                print()
                if waiting_user.username == username:
                    data['is_confirm'] = False
                    serializer = WaitingSerializer(waiting_user, data=data)
                    if serializer.is_valid(raise_exception=True):
                        waiting = serializer.save()
                        # send_mail(
                        #     'Themevler 인증메일입니다.',         # 제목
                        #     str(confirm_code), # 내용
                        #     'from@example.com',     
                        #     ['gagle637@gmail.com'],     # 받는 이메일 리스트
                        #     fail_silently=False,
                        # )
                        return Response({'message' : ['메일 재전송 완료.']})
                    return Response({'message' : ['메일 전송에 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)
            serializer = WaitingSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                # send_mail(
                #     'Themevler 인증메일입니다.',         # 제목
                #     str(confirm_code), # 내용
                #     'from@example.com',     
                #     ['gagle637@gmail.com'],     # 받는 이메일 리스트
                #     fail_silently=False,
                # )
                waiting = serializer.save()
                return Response({'message' : ['메일 전송 완료.']})
            return Response({'message' : ['메일 전송에 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':['이미 가입된 이메일입니다.']},status=status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny, ))
class Nickname(APIView):
    def get(self, request, format=None):
        serializer = UserNicknameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message' : ['사용하실수 있는 닉네임입니다.']})
        return Response({'message' : ['닉네임 중복체크를 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny, ))
class Username(APIView):
    def get(self, request, format=None):
        serializer = UsernameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message' : ['사용하실수 있는 이메일입니다.']})
        return Response({'message' : ['아이디 중복체크를 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((AllowAny, ))
class SignUp(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        if Waiting.objects.filter(username=username).exists():
            waiting_user = Waiting.objects.get(username=username)
            if waiting_user.username == username and waiting_user.is_confirm:
                if waiting_user.updated_at > datetime.now(timezone.utc) - timedelta(minutes=10):
                    serializer = UserCreationSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        user = serializer.save()
                        user.set_password(request.data.get('password'))
                        user.save()
                        return Response({'message' : ['환영합니다! 회원가입이 정상적으로 처리되었습니다.']})
                else:
                    return Response({'message' : ['유효시간이 지났습니다.']}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({'message' : ['인증이 되지 않은 회원입니다.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message' : ['회원가입이 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)


class UserMgmt(APIView):
    def delete(self, request, format=None):
        jwt_data = decoder(request.headers['Authorization'].split(' ')[1])
        user = get_object_or_404(User, id=jwt_data['user_id'])
        user.delete()
        return Response({'message' : ['회원탈퇴가 정상적으로 처리되었습니다.']}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, format=None):
        jwt_data = decoder(request.headers['Authorization'].split(' ')[1])
        user = get_object_or_404(User, id=jwt_data['user_id'])
        serializer = UserNicknameSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.save()
            return Response({'message' : ['회원정보가 정상적으로 변경되었습니다.']})
        return Response({'message' : ['회원정보 변경이 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)



class Password(APIView):
    def put(self, request, format=None):
        jwt_data = decoder(request.headers['Authorization'].split(' ')[1])
        user = get_object_or_404(User, id=jwt_data['user_id'])
        password_data = decoder(request.data.get('data'))
        serializer = UserPasswordSerializer(user, data=password_data)
        if serializer.is_valid(raise_exception=True):
            print(password_data)
            if user.check_password(password_data.get('original_password')):
                user = serializer.save()
                user.set_password(password_data.get('password'))
                user.save()
                return Response({'message' : ['회원정보가 정상적으로 변경되었습니다.']})
            return Response({'message' : ['비밀번호가 올바르지않습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message' : ['비밀번호 변경이 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)


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
