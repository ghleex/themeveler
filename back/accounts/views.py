from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserCreationSerializer, UserNicknameSerializer, WaitingSerializer, UsernameSerializer, ConfirmCodeSerializer
from .models import Waiting
from random import SystemRandom
from datetime import datetime, timedelta, timezone
import re

# Create your views here.
User = get_user_model()

class Mail(APIView):
    @permission_classes((AllowAny, ))
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
        waiting_user = Waiting.objects.filter(username=request.data.get('username')).first()
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

        
    @permission_classes((AllowAny, ))
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
            waiting_user = Waiting.objects.filter(username=username).first()
            if waiting_user and waiting_user.username == username:
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
            else:
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
            return Response({'message' : ['메일 전송에 실패하였습니다.']}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':['이미 가입된 이메일입니다.']},status=status.HTTP_400_BAD_REQUEST)

class Nickname(APIView):
    @permission_classes((AllowAny, ))
    def get(self, request, format=None):
        serializer = UserNicknameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message' : ['사용하실수 있는 닉네임입니다.']})
        return Response({'message' : ['닉네임 중복체크를 실패하였습니다.']}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Username(APIView):
    @permission_classes((AllowAny, ))
    def get(self, request, format=None):
        serializer = UsernameSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message' : ['사용하실수 있는 이메일입니다.']})
        return Response({'message' : ['아이디 중복체크를 실패하였습니다.']}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMgmt(APIView):
    @permission_classes((AllowAny, ))
    def post(self, request, format=None):
        username = request.data.get('username')
        waiting_user = Waiting.objects.filter(username=username).first()
        if waiting_user and waiting_user.username == username and waiting_user.is_confirm:
            serializer = UserCreationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.set_password(request.data.get('password'))
                user.save()
                return Response({'message' : ['회원가입이 성공적으로 완료되었습니다.']})
        else:
            return Response({'message' : ['인증이 되지 않은 회원입니다.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message' : ['아이디 생성이 실패하였습니다.']}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)


