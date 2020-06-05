from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, parser_classes
from rest_framework.parsers import FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_jwt.settings import api_settings
from drf_yasg.utils import swagger_auto_schema
from .models import NoticeCategory, Notice, VoiceCategory, CustomersVoice, ManagersReply, Comment, ReComment, ReportComment, ReportReComment
from .serializers import NoticeCategorySerializer, NoticeSerializer, VoiceCategorySerializer, CustomersVoiceSerializer
from .serializers import ManagerReplySerializer, CommentSerializer, ReCommentSerializer
from .serializers import ReportCommentSerializer, ReportReCommentSerializer
from articles.serializers import ManagerReplySerializer
from travels.models import Theme, Destination
from travels.serializers import ThemeSerializer, DestinationSerializer

User = get_user_model()
decoder = api_settings.JWT_DECODE_HANDLER

access_message = {
    'message': 'INVALID ACCESS'
}

error_message = {
    'message': 'AN ERROR HAS BEEN OCCURRED'
}

# Create your views here.
def get_user(token, format=None):
    jwt_data = decoder(token[1])
    user = get_object_or_404(User, id=jwt_data['user_id'])
    return user


@permission_classes((IsAuthenticated,))
class SetVoiceCategory(APIView):
    """
        고객센터(관리자) - "요청 유형" 항목 조회/생성

        ---
        # 내용
        ## 공통
            * categories: 전체 유형
        ## GET
            * category: 유형을 담을 리스트
        ## POST
            * category: 새롭게 만들 유형
    """
    def get(self, request, format=None):
        categories = VoiceCategory.objects.all()
        serializer_c = VoiceCategorySerializer(categories, many=True)
        return Response(serializer_c.data, status=status.HTTP_200_OK)


    def post(self, request, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        if not user.is_staff:
            return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)
        try:
            category = request.data.get('category')
            data = {
                'category': category,
            }
            serializer = VoiceCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
class ChangeVoiceCategory(APIView):
    """
        고객센터(관리자) - "요청 유형" 항목 수정/삭제

        ---
        # 내용
            * category: 요청 유형 QuerySet
        
    """
    def get_category(self, category_pk, format=None):
        return get_object_or_404(VoiceCategory, pk=category_pk)
        
    def put(self, request, category_pk, format=None):
        category = self.get_category(category_pk)
        try:
            category.category = request.data.get('category')
            data = {
                'category': category.category,
            }
            serializer = VoiceCategorySerializer(category, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_pk, format=None):
        category = self.get_category(category_pk)
        category.delete()
        message = {
            'message': 'SUCCESSFULLY DELETED THE CATEGORY'
        }
        return Response(message, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class CustomersVoices(APIView):
    """
        고객센터(사용자) - 요청 글 조회/등록

        ---
        # 내용
            * voices: 해당 유저의 고객센터 작성 글 QuerySet
        ## GET
            * return 값: voice 목록(요청자와 실제 사용자가 같은 경우) / 부적절한 엑세스 메시지(요청자와 실제 사용자가 다른 경우)
    """
    def get(self, request, user_pk, format=None):
        request_user = get_user(request.headers['Authorization'].split(' '))
        if user_pk == request_user.pk and not request_user.is_staff:
            voices = CustomersVoice.objects.filter(request_user=user_pk).order_by('-created_at')
            serializer_v = CustomersVoiceSerializer(voices, many=True)
            return Response(serializer_v.data, status=status.HTTP_200_OK)
        elif request_user.is_staff:
            voices = CustomersVoice.objects.all().order_by('-created_at')
            serializer_v = CustomersVoiceSerializer(voices, many=True)
            return Response(serializer_v.data, status=status.HTTP_200_OK)
        else:
            return Response(access_message, status=status.HTTP_403_FORBIDDEN)
            
    def post(self, request, user_pk, format=None):
        request_user = get_user(request.headers['Authorization'].split(' '))
        if user_pk == request_user.pk:
            requests = request.data
            data = {
                'title': requests.get('title'),
                'content': requests.get('content'),
                'category': requests.get('category'),
                'request_user': request_user.pk,
            }
            serializer = CustomersVoiceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)


@permission_classes((IsAuthenticated,))
class CustomersVoiceChange(APIView):
    """
        고객센터(사용자) - 요청 글 상세 내용 확인/수정/삭제
        
        ---
        # 내용
            * voice: 고객센터 내에서 사용자가 선택한 글
        ## PUT
            * return 값: voice.id
    """
    def get_voice(self, voice_pk, format=None):
        return get_object_or_404(CustomersVoice, pk=voice_pk)

    def get(self, request, voice_pk, format=None):
        request_user = get_user(request.headers['Authorization'].split(' '))
        voice = self.get_voice(voice_pk)
        try:
            if voice.request_user.pk == request_user.pk or request_user.is_staff:
                serializer_v = CustomersVoiceSerializer(voice)
                req_user = serializer_v['request_user']
                replys = voice.manager_reply.all()
                serializer_r = ManagerReplySerializer(replys, many=True)
                data = serializer_v.data
                data['replys'] = serializer_r.data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, voice_pk, format=None):
        request_user = get_user(request.headers['Authorization'].split(' '))
        voice = self.get_voice(voice_pk)
        if request_user.pk == voice.request_user.pk:
            requests = request.data
            voice.title = requests.get('title')
            voice.content = requests.get('content')
            data = {
                'title': voice.title,
                'content': voice.content,
                'category': requests.get('category'),
                'request_user': request_user.pk,
            }
            serializer = CustomersVoiceSerializer(voice, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(access_message, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, voice_pk, format=None):
        request_user = get_user(request.headers['Authorization'].split(' '))
        voice = self.get_voice(voice_pk)
        try:
            if voice.is_fixed:
                message = {
                    'message': 'CANNOT DELETE THE VOICE DUE TO ADMIN\'S REPLY'
                }
                return Response(message, status=status.HTTP_202_ACCEPTED)
            else:
                if request_user.pk == voice.request_user.pk:
                    voice.delete()
                    message = {
                        'message': 'SUCCESSFULLY DELETED THE VOICE'
                    }
                    return Response(message, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
class ManagersReplying(APIView):
    """
        고객센터(관리자) - 처리 내용 등록

        ---
        # 내용
            * manager: 관리자
    """
    def post(self, request, voice_pk, format=None):
        try:
            requests = request.data
            voice = get_object_or_404(CustomersVoice, pk=voice_pk)
            voice.is_fixed = True
            voice.save()
            data = {
                'content': requests.get('content'),
                'voice': voice_pk,
                'manager': request.user.pk,
            }
            serializer = ManagerReplySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
class ManagersReplyChange(APIView):
    """
        고객센터(관리자) - 관리자의 답변 수정
        
        ---
        # 내용
            * manager: 관리자
            * reply: 답변
    """
    def put(self, request, voice_pk, reply_pk, format=None):
        reply = get_object_or_404(ManagersReply, pk=reply_pk)
        try:
            requests = request.data
            reply.content = requests.get('content')
            data = {
                'content': reply.content,
                'voice': voice_pk,
                'manager': request.user.pk,
            }
            serializer = ManagerReplySerializer(reply, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
class SetNoticeCategory(APIView):
    """
        공지사항 유형 조회/생성

        ---
        # 내용
        ## 공통
            * categories: 전체 유형
        ## GET
            * category: 유형을 담을 리스트
        ## POST
            * category: 새롭게 만들 유형
    """
    def get(self, request, format=None):
        categories = NoticeCategory.objects.all()
        serializer_c = NoticeCategorySerializer(categories, many=True)
        user = get_user(request.headers['Authorization'].split(' '))
        if user.is_staff:
            return Response(serializer_c.data, status=status.HTTP_200_OK)
        else:
            return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        try:
            category = request.data.get('category')
            data = {
                'category': category,
            }
            serializer = NoticeCategorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
class ChangeNoticeCategory(APIView):
    """
        공지사항 유형 수정/삭제

        ---
        # 내용
            * category: 요청 유형 QuerySet
        
    """
    def get_category(self, category_pk, format=None):
        return get_object_or_404(NoticeCategory, pk=category_pk)
        
    def put(self, request, category_pk, format=None):
        category = self.get_category(category_pk)
        try:
            category.category = request.data.get('category')
            data = {
                'category': category.category,
            }
            serializer = NoticeCategorySerializer(category, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_pk, format=None):
        category = self.get_category(category_pk)
        category.delete()
        message = {
            'message': 'SUCCESSFULLY DELETED THE NOTICE CATEGORY'
        }
        return Response(message, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class Notices(APIView):
    """
        전체 공지사항 - 목록과 게시

        ---
        # 내용
          * isNoticeAll: True 인 것만 출력
    """
    def get(self, request, format=None):
        notices = Notice.objects.filter(isNoticeAll=True).order_by('-writed_at')
        serializer_n = NoticeSerializer(notices, many=True)
        return Response(serializer_n.data, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class NoticeView(APIView):
    """
        개별 공지사항 보기

        ---
    """
    def get_object(self, notice_pk, format=None):
        return get_object_or_404(Notice, pk=notice_pk)

    def get(self, request, notice_pk, format=None):
        notice = self.get_object(notice_pk)
        try:
            serializer_n = NoticeSerializer(notice)
            return Response(serializer_n.data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes((IsAuthenticated, ))
class ThemeNoticesView(APIView):
    """
        코스 공지사항 전체 목록 - 사용자/관리자 공통

        ---

    """
    def get_theme(self, theme_pk, format=None):
        return get_object_or_404(Theme, pk=theme_pk)
    
    def get(self, request, theme_pk, format=None):
        theme = self.get_theme(theme_pk)
        try:
            notices = theme.theme_notices.all().order_by('-writed_at')
            serializer_n = NoticeSerializer(notices, many=True)
            return Response(serializer_n.data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
class ThemeNoticesPost(APIView):
    """
        코스 공지사항 작성 - 관리자 화면

        ---
    """
    def post(self, request, format=None):
        try:
            requests = request.data
            data = {
                'title': requests.get('title'),
                'content': requests.get('content'),
                'category': requests.get('category'),
                'writer': request.user.pk,
                'theme': requests.get('theme'),
                'isNoticeAll': requests.get('isNoticeAll'),
            }
            serializer = NoticeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class ThemeNoticesChange(APIView):
    """
        코스 공지사항 - 세부 내용(공통) | 관리자의 수정/삭제    
        
        ---
    """
    def get_notices(self, notice_pk, format=None):
        return get_object_or_404(Notice, pk=notice_pk)        

    def get(self, request, notice_pk, format=None):
        notice = self.get_notices(notice_pk)
        serializer_n = NoticeSerializer(notice)
        return Response(serializer_n.data, status=status.HTTP_200_OK)
    
    def put(self, request, notice_pk, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        if not user.is_staff:
            return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)
        notice = self.get_notices(notice_pk)
        try:
            if request.user == notice.writer:
                requests = request.data
                notice.title = requests.get('title')
                notice.content = requests.get('content')
                notice.writer_id = request.user.pk
                data = {
                    'title': notice.title,
                    'content': notice.content,
                    'category': requests.get('category'),
                    'writer': notice.writer_id,
                    'theme': requests.get('theme'),
                }
                serializer = NoticeSerializer(notice, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, notice_pk, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        if not user.is_staff:
            return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)
        try:
            notice = self.get_notices(notice_pk)
            if request.user == notice.writer:
                notice.delete()
                message = {
                    'message': 'SUCCESSFULLY DELETED THE NOTICE'
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))
class Search(APIView):
    """
        검색 - 테마, 여행지

        ---
    """
    def get(self, request, searching_word, format=None):
        try:
            query = searching_word
            result = {
                'theme': '검색할 내용이 존재하지 않습니다.',
                'dest': '검색할 내용이 존재하지 않습니다.',
            }        
            
            theme_results = Theme.objects.filter(
                Q(name__contains=query) | Q(content__contains=query) | Q(region__contains=query) | Q(dests__icontains=query)
            ).distinct()
            dest_results = Destination.objects.filter(
                Q(name__contains=query)
            ).distinct()
            result['theme'] = ThemeSerializer(theme_results, many=True).data
            result['dest'] = DestinationSerializer(dest_results, many=True).data
            return Response(result, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class CommentSelf(APIView):
    """
        자신이 작성한 댓글 목록

        ---
    """
    def get(self, request, user_pk, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        try:
            comments = Comment.objects.filter(writer=user.pk).order_by('-writed_at')
            serializer_c = CommentSerializer(comments, many=True)
            return Response(serializer_c.data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class Comments(APIView):
    """
        댓글 - 목록과 작성

        ---
    """
    def get_dest(self, dest_pk, format=None):
        return get_object_or_404(Destination, pk=dest_pk)

    def get(self, request, dest_pk, format=None):
        dest = self.get_dest(dest_pk)
        try:
            comments = dest.destination_comments.all().order_by('-writed_at')
            serializer_c = CommentSerializer(comments, many=True)
            return Response(serializer_c.data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, dest_pk, format=None):
        dest = self.get_dest(dest_pk)
        try:
            requests = request.data
            data = {
                'content': requests.get('content'),
                'writer': request.user.pk,
                'destination': dest_pk,
            }
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                comment = serializer.save()
                comment.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class CommentChange(APIView):
    """
        댓글 - 수정과 삭제

        ---
    """
    def get_comment(self, comment_pk, format=None):
        return get_object_or_404(Comment, pk=comment_pk)

    def put(self, request, comment_pk, format=None):
        comment = self.get_comment(comment_pk)
        try:
            comment.content = request.data.get('content')
            data = {
                'content': comment.content,
                'writer': comment.writer_id,
                'destination': comment.destination_id,
            }
            serializer = CommentSerializer(comment, data=data)
            if serializer.is_valid():
                comment = serializer.save()
                comment.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_pk, format=None):
        comment = self.get_comment(comment_pk)
        try:
            if request.user == comment.writer:
                comment.delete()
                message = {
                    'message': 'SUCCESSFULLY DELETED THE COMMENT'
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class ReCommentSelf(APIView):
    """
        자신이 작성한 대댓글(댓글의 댓글) 목록

        ---
    """
    def get(self, request, user_pk, format=None):
        user = get_user(request.headers['Authorization'].split(' '))
        try:
            recomments = ReComment.objects.filter(writer=user.pk).order_by('-writed_at')
            serializer_r = ReCommentSerializer(recomments, many=True)
            return Response(serializer_r.data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class ReComments(APIView):
    """
        대댓글 - 목록과 작성

        ---
    """
    def get_comment(self, comment_pk, format=None):
        return get_object_or_404(Comment, pk=comment_pk)

    def get(self, request, comment_pk, format=None):
        comment = self.get_comment(comment_pk)
        try:
            recomments = comment.recomments_original.all().order_by('-writed_at')
            serializer_r = ReCommentSerializer(recomments, many=True)
            return Response(serializer_r.data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, comment_pk, format=None):
        try:
            data = {
                'content': request.data.get('content'),
                'comment': comment_pk,
                'writer': request.user.pk,
            }
            serializer = ReCommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class ReCommentChange(APIView):
    """
        대댓글 - 수정과 삭제

        ---
    """
    def get_recomment(self, recomment_pk, format=None):
        return get_object_or_404(ReComment, pk=recomment_pk)

    def put(self, request, recomment_pk, format=None):
        recomment = self.get_recomment(recomment_pk)
        try:
            recomment.content = request.data.get('content')
            data = {
                'content': recomment.content,
                'comment': recomment.comment_id,
                'writer': request.user.pk,
            }
            serializer = ReCommentSerializer(recomment, data=data)
            if serializer.is_valid():
                re_comment = serializer.save()
                re_comment.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recomment_pk, format=None):
        recomment = self.get_recomment(recomment_pk)
        try:
            if request.user == recomment.writer:
                recomment.delete()
                message = {
                    'message': 'SUCCESSFULLY DELETED THE RECOMMENT'
                }
                return Response(message, status=status.HTTP_200_OK)
            else:
                return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)        


class ReportCommentMgmt(APIView):
    @swagger_auto_schema(request_body=ReportCommentSerializer)
    def post(self, request, comment_pk, format=None):
        """
            댓글 신고 - 해당 댓글을 신고합니다.

            # 내용
                report_text: 신고 내용을 작성합니다.
                user: 해당 유저의 user_id 값을 작성합니다. Int 형식이어야 합니다.
                comment_pk: 해당 댓글의 comment_id 값을 작성합니다. Int 형식이어야 합니다.
        """
        user = get_user(request.headers['Authorization'].split(' '))
        try:
            Comment.objects.get(pk=comment_pk)
        except:
            return Response({'message': ['해당 댓글은 존재하지 않습니다.']}, status=status.HTTP_404_NOT_FOUND)
        if not ReportComment.objects.filter(comment=comment_pk, user=user.id).exists():
            data = {
                'user': user.id,
                'comment': comment_pk,
                'report_text': request.data.get('report_text')
            }
            serializer = ReportCommentSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': ['해당 댓글이 성공적으로 신고되었습니다.']})
            return Response({'message': ['해당 댓글에 대한 신고가 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': ['이미 신고가 접수된 댓글입니다.']}, status=status.HTTP_400_BAD_REQUEST)


class ReportReCommentMgmt(APIView):
    @swagger_auto_schema(request_body=ReportReCommentSerializer)
    def post(self, request, recomment_pk, format=None):
        """
            대댓글 신고 - 해당 대댓글을 신고합니다.

            # 내용
                report_text: 신고 내용을 작성합니다.
                user: 해당 유저의 user_id 값을 작성합니다. Int 형식이어야 합니다.
                recomment_pk: 해당 댓글의 recomment_id 값을 작성합니다. Int 형식이어야 합니다.
        """
        user = get_user(request.headers['Authorization'].split(' '))
        try:
            ReComment.objects.get(pk=recomment_pk)
        except:
            return Response({'message': ['해당 대댓글은 존재하지 않습니다.']}, status=status.HTTP_404_NOT_FOUND)
        if not ReportReComment.objects.filter(user=user.id).exists():
            data = {
                'user': user.id,
                're_comment': recomment_pk,
                'report_text': request.data.get('report_text')
            }
            serializer = ReportReCommentSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': ['해당 댓글이 성공적으로 신고되었습니다.']})
            return Response({'message': ['해당 댓글에 대한 신고가 실패하였습니다.']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': ['이미 신고가 접수된 댓글입니다.']}, status=status.HTTP_400_BAD_REQUEST)
