from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import obtain_jwt_token
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserCreationSerializer, UserNicknameSerializer, WaitingSerializer
from .serializers import UsernameSerializer, ConfirmCodeSerializer, UserPasswordSerializer
from .serializers import UserSignInSerializer, UserBanSerializer
from .models import Waiting
from random import SystemRandom, choice
from datetime import datetime, timedelta
from decouple import config
from google.oauth2 import id_token
from google.auth.transport import requests as req
import json
import requests
import re


# Create your views here.
User = get_user_model()
decoder = api_settings.JWT_DECODE_HANDLER
encoder = api_settings.JWT_ENCODE_HANDLER
payload = api_settings.JWT_PAYLOAD_HANDLER

# prefix, suffix: SignUp - anonymous
prefix = [
    '게으른 ', '쾌활한 ', '유쾌한 ', '아름다운 ', '부지런한 ', '예쁜 ', '근면한 ', 
    '무서운 ', '우스운 ', '아리따운 ', '자비로운 ', '자애로운 ', '우아한 ', '소환된 ',
    '떠돌아다니는 ', 
]
suffix = [
    '사자 ', '호랑이 ', '독수리 ', '개미핥기 ', '상어 ', '고양이 ', '기린 ',
    '치타 ', '표범 ', '코끼리 ', '고릴라 ', '원숭이 ', '강아지 ', '펭귄 ',
]

email_check = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

back_url = config('BACK_URL')
front_url = config('FRONT_URL')

def check_request(request, check_list):
    data = {}
    for form in check_list:
        value = request.get(form)
        if not value:
            data[form] = ['이 필드는 필수항목 입니다.']
        elif form == 'username':
            if email_check.match(value) == None:
                data[form] = ['Email 형식이 아닙니다.']
        elif form == 'banning_period':
            if not value.isdigit():
                data[form] = ['이 필드는 Int 형식이여야 합니다.']
    return data


def get_user(token, format=None):
    jwt_data = decoder(token[1])
    user = get_object_or_404(User, id=jwt_data['user_id'])
    return user


@permission_classes((AllowAny, ))
class EmailAuth(APIView):
    def get(self, request, username, confirm_code, format=None):
        """
            인증메일(확인) - 발송된 인증 메일을 확인합니다.

            # 내용
                * username: Email 형식이어야 합니다.
                * confirm_code: '-' 포함 12자리의 숫자입니다.
        """
        if email_check.match(username) == None:
            return Response({'message': ['username이 Email 형식이 아닙니다.']}, status=status.HTTP_400_BAD_REQUEST)
        if Waiting.objects.filter(username=username).exists():
            waiting_user = Waiting.objects.get(username=username)
            if waiting_user.is_confirm:
                return Response({'message': ['이미 인증된 유저입니다.']}, status=status.HTTP_400_BAD_REQUEST)
            if waiting_user.username == username and waiting_user.confirm_code == confirm_code:
                if waiting_user.updated_at > datetime.now() - timedelta(minutes=10):
                    waiting_user.is_confirm = True
                    waiting_user.confirm_code = None
                    waiting_user.save()
                    return Response({'message': ['메일 인증에 성공하였습니다..']}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': ['유효시간이 지났습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': ['인증에 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))
class EmailSend(APIView):
    def mail_send(self, data):
        subject = 'Themevler 인증메일입니다.'
        html_message = render_to_string('keyMail.html', {'confirm_code': data.get('confirm_code')})
        plain_message = strip_tags(html_message)
        from_email = '<from@example.com>'
        to = data.get('username')
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        

    @swagger_auto_schema(request_body=WaitingSerializer)
    def post(self, request, format=None):
        """
            인증메일(발송) - 인증 메일을 발송합니다.
            

            # 내용
                * username: Email 형식이어야 합니다.
        """
        if UsernameSerializer(data=request.data).is_valid(raise_exception=True):
            confirm_code = ''
            username = request.data.get('username')
            for cnt in range(3):
                sr = SystemRandom()
                confirm_code += str(sr.choice(range(1000, 10000)))
                if cnt != 2:
                    confirm_code += '-'
            data = {
                'username': username,
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
                        return Response({'message': ['메일 재전송 완료.']}, status=status.HTTP_200_OK)
                    return Response({'message': ['메일 전송에 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)
            serializer = WaitingSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                self.mail_send(data)
                waiting = serializer.save()
                return Response({'message': ['메일 전송 완료.']}, status=status.HTTP_200_OK)
            return Response({'message': ['메일 전송에 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': ['이미 가입된 이메일입니다.']},status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))
class Nickname(APIView):
    """
        닉네임 중복체크 - 닉네임의 중복을 체크합니다.

        # 내용
            * nickname: 최대 20자의 String을 받습니다.
    """
    def get(self, request, nickname, format=None):
        data = {
            'nickname': nickname
        }
        serializer = UserNicknameSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message': ['사용하실수 있는 닉네임입니다.']}, status=status.HTTP_200_OK)
        return Response({'message': ['닉네임 중복체크를 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))
class Username(APIView):
    """
        아이디 중복체크 - 아이디를 중복체크합니다.

        # 내용
            * username: Email 형식이어야 합니다.
    """
    def get(self, request, username, format=None):
        data = {
            'username': username
        }
        serializer = UsernameSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message': ['사용하실수 있는 이메일입니다.']})
        return Response({'message': ['아이디 중복체크를 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))
class SignUp(APIView):
    @swagger_auto_schema(request_body=UserCreationSerializer)
    def post(self, request, format=None):
        """
            회원 가입 - 회원정보를 생성합니다.

            # 내용
                * username: Email 형식이어야 합니다.
                * nickname: 최대 20자의 String을 받습니다.
                * password: 8자 이상이어야 합니다.
                            1자 이상 문자가 포함되어야합니다.
                            보안이 취약한 비밀번호는 사용할 수 없습니다. (예: 12345678)
        """
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
                    return Response({'message': ['환영합니다! 회원가입이 정상적으로 처리되었습니다.']}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': ['유효시간이 지났습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': ['인증이 되지 않은 회원입니다.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': ['회원가입이 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated, ))
class UserMgmt(APIView):
    def delete(self, request, format=None):
        """
            회원탈퇴 - 회원정보를 삭제합니다.

            # 내용
                * headers에서 포함된 jwt 데이터의 user_id를 이용합니다.
        """
        user = get_user(request.headers['Authorization'].split(' '))
        user.delete()
        return Response({'message': ['회원탈퇴가 정상적으로 처리되었습니다.']}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=UserNicknameSerializer)
    def put(self, request, format=None):
        """
            회원정보수정 - 회원정보를 수정합니다.

            # 내용
                * headers에서 포함된 jwt 데이터의 user_id를 이용합니다.
                * nickname: 최대 20자의 String을 받습니다.
        """
        user = get_user(request.headers['Authorization'].split(' '))
        serializer = UserNicknameSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.save()
            return Response({'message': ['회원정보가 정상적으로 변경되었습니다.']}, status=status.HTTP_200_OK)
        return Response({'message': ['회원정보 변경이 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated, ))
class Password(APIView):
    @swagger_auto_schema(request_body=UserPasswordSerializer)
    def put(self, request, format=None):
        """
            비밀번호 변경 - 유저의 비밀번호를 변경합니다.

            # 내용
                * headers에서 포함된 jwt 데이터의 user_id를 이용합니다.
                * password: 8자 이상이어야 합니다.
                            1자 이상 문자가 포함되어야합니다.
                            보안이 취약한 비밀번호는 사용할 수 없습니다. (예: 12345678)
        """
        jwt_data = decoder(request.headers['Authorization'].split(' ')[1])
        user = get_object_or_404(User, id=jwt_data['user_id'])
        if not user.has_usable_password():
            return Response({'message': ['소셜 로그인 유저는 비밀번호를 변경할 수 없습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        password_data = decoder(request.data.get('data'))
        serializer = UserPasswordSerializer(user, data=password_data)
        if serializer.is_valid(raise_exception=True):
            if user.check_password(password_data.get('original_password')):
                user = serializer.save()
                user.set_password(password_data.get('password'))
                user.save()
                return Response({'message': ['회원정보가 정상적으로 변경되었습니다.']}, status=status.HTTP_200_OK)
            return Response({'message': ['비밀번호가 올바르지않습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': ['비밀번호 변경이 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))
class SignIn(APIView):
    @swagger_auto_schema(request_body=UserSignInSerializer)
    def post(self, request, format=None):
        """
            로그인

            # 내용
                * 회원가입에서 생성한 유저정보를 작성합니다.
                * return: jwt가 반환됩니다.
        """
        username = request.data.get('username')
        sign_in_user = get_object_or_404(User, username=username)
        if not sign_in_user.has_usable_password():
            return Response({'message': ['해당 유저는 소셜로그인 유저입니다.']}, status=status.HTTP_400_BAD_REQUEST)
        if sign_in_user.banning_period:
            if str(sign_in_user.banning_period) < datetime.today().strftime('%Y-%m-%d'):
                sign_in_user.is_active = True
                sign_in_user.banning_period = None
                sign_in_user.save()
            else:
                sign_in_user.is_active = False
                sign_in_user.save()
                return Response({'message': ['해당 유저는 ' + str(sign_in_user.banning_period) + '까지 접근이 제한되었습니다.' ]}, status=status.HTTP_401_UNAUTHORIZED)
        login_response = obtain_jwt_token(request._request)
        token = login_response.data.get('token')
        if not token:
            return login_response
        return Response({'nickname': sign_in_user.nickname, 'is_staff': sign_in_user.is_staff, 'token': token, 'anonymous': sign_in_user.anonymous}, status=status.HTTP_200_OK)


@permission_classes((IsAdminUser, ))
class UserBan(APIView):
    @swagger_auto_schema(request_body=UserBanSerializer)
    def post(self, request, user_pk, format=None):
        """
            유저 정지(관리자) - 유저의 접근을 금지 처리합니다.

            # 내용
                * user_pk: Int 형식이어야 합니다.
                * banning_period: Int 형식이어야 합니다. N일 후까지 접근을 금지합니다.
        """
        sign_in_user = User.objects.get(id=user_pk)
        sign_in_user.banning_period = (datetime.today() + timedelta(days=int(request.data.get('banning_period')))).strftime('%Y-%m-%d')
        sign_in_user.is_active = False
        sign_in_user.save()
        return Response({'message': [sign_in_user.username + '가 '+ sign_in_user.banning_period + '까지 정지처리 되었습니다.']}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UsernameSerializer)
    def delete(self, request, user_pk, format=None):
        """
            유저 정지 취소(관리자) - 유저 접근 금지 처리를 취소합니다.

            # 내용
                * user_pk: Int 형식이어야 합니다.
        """
        sign_in_user = User.objects.get(id=user_pk)
        sign_in_user.banning_period = None
        sign_in_user.is_active = True
        sign_in_user.save()
        return Response({'message': [sign_in_user.username + '님의 정지처리가 취소되었습니다.']}, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class KakaoSignInView(APIView):
    def get(self, request):
        """
            카카오 로그인

            # 내용
                * 주소로 직접 접근해야 합니다.

        """
        client_id = config('KAKAO_REST_API_KEY')
        redirect_uri = f'{back_url}/api/accounts/social/kakao/callback/'
        url = f'https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
        return redirect(url)


@permission_classes((AllowAny, ))
class KakaoSignInCallbackView(APIView):
    def get(self, request):
        """
            카카오 콜백

            ___
        """
        try:
            code = request.GET.get('code')                                
            client_id = config('KAKAO_REST_API_KEY')
            redirect_uri = f'{back_url}/api/accounts/social/kakao/callback/'
            url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}'
            token_request = requests.get(url)
            token_json = token_request.json()                                 
            access_token = token_json.get('access_token')        
            error = token_json.get('error', None)
            if error is not None:
                return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'message': 'INVALID_TOKEN'}, status=status.HTTP_400_BAD_REQUEST)
        except access_token.DoesNotExist:
            return Response({'message': 'INVALID_TOKEN'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile_request = requests.get(                          
            'https://kapi.kakao.com/v2/user/me', headers={'Authorization': f'Bearer {access_token}'},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get('kakao_account')
        email = kakao_account.get('email', None)                   
        kakao_id = profile_json.get('id')
        data = {
            'username': email
        }
        social_user = User.objects.filter(username=email).first()
        if social_user and social_user.username == email:
            if not social_user.has_usable_password():
                user = social_user
            else:
                return redirect(f'{front_url}/login/')
        else:
            serializer = UsernameSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.set_unusable_password()
                user.nickname = 'KAKAO 유저 ' + str(user.id)
                user.anonymous = choice(prefix) + choice(suffix) + str(user.id)
                user.save()
        jwt = encoder(payload(user))
        data = {
            'nickname': user.nickname,
            'anonymous': user.anonymous
        }
        jwt_data = encoder(data)
        return redirect(f'{front_url}/checktoken/{jwt_data}/{jwt}/') 


@permission_classes((AllowAny, ))
class GoogleSignInView(APIView):
    def get(self, request):
        """
            구글 소셜 로그인
            
            # 내용
                * 주소로 직접 접근해야 합니다.
        """
        base = 'https://accounts.google.com/o/oauth2/v2/auth?'
        client_id = config('GOOGLE_APP_ID')
        urls = [
            f'redirect_uri={back_url}/api/accounts/social/google/callback/&',
            'prompt=consent&response_type=code&',
            f'client_id={client_id}&'
            'scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&',
            'access_type=offline',
        ]
        for url in urls:
            base += url
        return redirect(base)


@permission_classes((AllowAny, ))
class GoogleSignInCallbackView(APIView):
    def get(self, request, format=None):
        """
            구글 콜백

            ---
        """
        google_access_code = request.GET.get('code', None)
        url = 'https://www.googleapis.com/oauth2/v4/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            'code': f'{google_access_code}',
            'client_id': config('GOOGLE_APP_ID'),
            'client_secret': config('GOOGLE_SECRET_KEY'),
            'redirect_uri': f'{back_url}/api/accounts/social/google/callback/',
            'grant_type': 'authorization_code',
        }
        google_response = requests.post(url, headers=headers, data=body)
        google_response_dict = json.loads(google_response.text)
        access_token = google_response_dict.get('access_token')
        id_info = id_token.verify_oauth2_token(google_response_dict.get('id_token'), req.Request(), config('GOOGLE_APP_ID'))
        email = id_info['email']
        data = {
            'username': email
        }
        social_user = User.objects.filter(username=email).first()
        if social_user and social_user.username == email:
            if not social_user.has_usable_password():
                user = social_user
            else:
                return redirect(f'{front_url}/login/')
        else:
            serializer = UsernameSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.set_unusable_password()
                user.nickname = 'GOOGLE 유저 ' + str(user.id)
                user.anonymous = choice(prefix) + choice(suffix) + str(user.id)
                user.save()
        jwt = encoder(payload(user))
        data = {
            'nickname': user.nickname,
            'anonymous': user.anonymous
        }
        jwt_data = encoder(data)
        return redirect(f'{front_url}/checktoken/{jwt_data}/{jwt}/')


@permission_classes((AllowAny, ))
class PasswordFind(APIView):
    def mail_send(self, data):
        subject = 'Themevler ' + data.get('username') + '님의 새로운 비밀번호입니다.'
        html_message = render_to_string('passwordMail.html', {'password': data.get('password')})
        plain_message = strip_tags(html_message)
        from_email = '<from@example.com>'
        to = data.get('username')
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    def get(self, request, username):
        """
            새로운 비밀번호를 계정으로 발송합니다.

            # 내용
                * username: Email 형식이어야 합니다.
        """
        if email_check.match(username) == None:
            return Response({'message': ['email 형식이 아닙니다.']}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(username=username).first()
        if user and user.username == username and user.has_usable_password():
            password = User.objects.make_random_password(length=14)
            data = {
                'username': username,
                'password': password
            }
            user.set_password(password)
            user.save()
            self.mail_send(data=data)
            return Response({'message': [username + '님에게 비밀번호를 전송했습니다.']}, status=status.HTTP_200_OK)
        else:
            return Response({'message': ['해당 유저는 회원 가입된 유저가 아니거나 소셜 로그인 유저입니다.']}, status=status.HTTP_400_BAD_REQUEST)
