from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_jwt.views import obtain_jwt_token
from .serializers import UserCreationSerializer, UserNicknameSerializer, WaitingSerializer
from .serializers  import UsernameSerializer, ConfirmCodeSerializer, UserPasswordSerializer
from .models import Waiting
from travels.serializers import MessageSerializer
from random import SystemRandom, choice
from datetime import datetime, timedelta, timezone
import re


# Create your views here.
User = get_user_model()
decoder = api_settings.JWT_DECODE_HANDLER
prefix = [
        '게으른 ', '쾌화한 ', '유쾌한 ', '아름다운 ', '부지런한 ', '예쁜 ', '근면한 ', 
        '무서운 ', '우스운 ', '아리따운 ', '자비로운 ', '자애로운 ', '우아한 '
        ]
suffix = ['사자', '호랑이', '독수리', '개미핥기', '상어', '고양이', '기린', '치타', '표범', '코끼리', '고릴라', '원숭이', '강아지']

def Check_request(request, check_list):
    data = {}
    for form in check_list:
        value = request.get(form)
        if not value:
            data[form] = ['이 필드는 필수항목 입니다.']
        elif form == 'username':
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if p.match(value) == None:
                data[form] = ['email형식이 아닙니다.']
        elif form == 'banning_period' and not value.isdigit():
            data[form] = ['이 필드는 INT형식이여야 합니다.']
    return data


@permission_classes((AllowAny, ))
class Mail(APIView):
    def mail_send(self, data):
        subject = 'Themevler 인증메일입니다.'
        html_message = render_to_string('keyMail.html', {'confirm_code': data.get('confirm_code')})
        plain_message = strip_tags(html_message)
        from_email = '<from@example.com>'
        to = data.get('username')
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)    

    def get(self, request, format=None):
        check_result = Check_request(request.data, ['username', 'confirm_code'])
        if check_result:
            return Response(check_result, status=status.HTTP_400_BAD_REQUEST)
        if Waiting.objects.filter(username=request.data.get('username')).exists():
            waiting_user = Waiting.objects.get(username=request.data.get('username'))
            if waiting_user.is_confirm:
                return Response({'message' : ['이미 인증된 유저입니다.']})
            if waiting_user.username == request.data.get('username') and waiting_user.confirm_code == request.data.get('confirm_code'):
                if waiting_user.updated_at > datetime.now() - timedelta(minutes=10):
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
            if Waiting.objects.filter(username=username).exists():
                waiting_user = Waiting.objects.get(username=username)
                if waiting_user.username == username:
                    data['is_confirm'] = False
                    serializer = WaitingSerializer(waiting_user, data=data)
                    if serializer.is_valid(raise_exception=True):
                        waiting = serializer.save()
                        self.mail_send(data)
                        return Response({'message' : ['메일 재전송 완료.']})
                    return Response({'message' : ['메일 전송에 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)
            serializer = WaitingSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                self.mail_send(data)
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
                if waiting_user.updated_at > datetime.now() - timedelta(minutes=10):
                    serializer = UserCreationSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        user = serializer.save()
                        user.set_password(request.data.get('password'))
                        user.anonymous = choice(prefix) + choice(suffix) + str(user.id)
                        user.save()
                    return Response({'message' : ['환영합니다! 회원가입이 정상적으로 처리되었습니다.']})
                else:
                    return Response({'message' : ['유효시간이 지났습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message' : ['인증이 되지 않은 회원입니다.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message' : ['회원가입이 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)

class UserMgmt(APIView):
    def get_user(self, token, format=None):
        jwt_data = decoder(token[1])
        user = get_object_or_404(User, id=jwt_data['user_id'])
        return user

    def delete(self, request, format=None):
        user = self.get_user(request.headers['Authorization'].split(' '))
        user.delete()
        return Response({'message' : ['회원탈퇴가 정상적으로 처리되었습니다.']}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, format=None):
        user = self.get_user(request.headers['Authorization'].split(' '))
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
            if user.check_password(password_data.get('original_password')):
                user = serializer.save()
                user.set_password(password_data.get('password'))
                user.save()
                return Response({'message' : ['회원정보가 정상적으로 변경되었습니다.']})
            return Response({'message' : ['비밀번호가 올바르지않습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message' : ['비밀번호 변경이 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))
class SignIn(APIView):
    def post(self, request, format=None):
        username=request.data.get('username')
        if User.objects.filter(username=username).exists():
            sign_in_user = User.objects.get(username=username)
            if sign_in_user.banning_period and str(sign_in_user.banning_period) < datetime.today().strftime('%Y-%m-%d'):
                sign_in_user.is_active = True
                sign_in_user.banning_period = None
            sign_in_user.save()
        return obtain_jwt_token(request._request)


@permission_classes((IsAdminUser, ))
class UserBan(APIView):
    def post(self, request, format=None):
        check_result = Check_request(request.data, ['username', 'banning_period',])
        if check_result:
            return Response(check_result, status=status.HTTP_400_BAD_REQUEST)
        username = request.data.get('username')
        sign_in_user = User.objects.get(username=username)
        sign_in_user.banning_period = (datetime.today() + timedelta(days=int(request.data.get('banning_period')))).strftime('%Y-%m-%d')
        sign_in_user.is_active = False
        sign_in_user.save()
        return Response({'message' : [username + '가 '+ sign_in_user.banning_period + '까지 정지처리 되었습니다.']})

    def delete(self, request, format=None):
        check_result = Check_request(request.data, ['username'])
        if check_result:
            return Response(check_result, status=status.HTTP_400_BAD_REQUEST)
        username=request.data.get('username')
        sign_in_user = User.objects.get(username=username)
        sign_in_user.banning_period = None
        sign_in_user.is_active = True
        sign_in_user.save()
        return Response({'message' : [username + '의 정지처리가 취소되었습니다.']})

