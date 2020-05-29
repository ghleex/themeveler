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


@permission_classes((IsAdminUser,))
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
        category = [VoiceCategorySerializer(c).data for c in categories]
        user = get_user(request.headers['Authorization'].split(' '))
        if user.is_staff:
            data = {
                'data': category,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
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
        if user_pk == request_user.pk:
            voices = CustomersVoice.objects.filter(request_user=user_pk).order_by('-created_at')
            voice = [CustomersVoiceSerializer(v).data for v in voices]
            data = {
                'voice': voice,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(access_message, status=status.HTTP_403_FORBIDDEN)
            
    def post(self, request, user_pk, format=None):
        request_user = get_user(request.headers['Authorization'].split(' '))
        if user_pk == request_user.pk:
            user = request_user.pk
            requests = request.data
            data = {
                'title': requests.get('title'),
                'content': requests.get('content'),
                'category': requests.get('category'),
                'request_user': user,
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

    def get(self, request, user_pk, voice_pk, format=None):
        request_user = get_user(request.headers['Authorization'].split(' '))
        voice = self.get_voice(voice_pk)
        try:
            if user_pk == request_user.pk:
                serializer_v = CustomersVoiceSerializer(voice).data
                req_user = serializer_v['request_user']
                data = {
                    'id': serializer_v['id'],
                    'title': serializer_v['title'],
                    'content': serializer_v['content'],
                    'category': serializer_v['category'],
                    'request_user_id': req_user,
                    'request_user_nickname': str(User.objects.get(pk=req_user).nickname),
                    'manager': serializer_v['manager'],
                    'is_fixed': serializer_v['is_fixed'],
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, user_pk, voice_pk, format=None):
        request_user = get_user(request.headers['Authorization'].split(' '))
        voice = self.get_voice(voice_pk)
        if request_user.pk == voice.request_user:
            requests = request.data
            voice.title = requests.get('title')
            voice.content = requests.get('content')
            voice.category = VoiceCategory.objects.get(pk=requests.get('category'))
            data = {
                'title': voice.title,
                'content': voice.content,
                'category': voice.category,
            }
            serializer = CustomersVoiceSerializer(voice, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(voice.id, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(access_message, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, user_pk, voice_pk, format=None):
        request_user = get_user(request.headers['Authorization'].split(' '))
        voice = self.get_voice(voice_pk)
        try:
            if voice.is_fixed:
                message = {
                    'message': 'CANNOT DELETE THE VOICE DUE TO ADMIN\'S REPLY'
                }
                return Response(message, status=status.HTTP_202_ACCEPTED)
            else:
                if request_user.pk == voice.request_user:
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
        고객센터(관리자) - 처리할 일 목록/등록

        ---
        # 내용
            * manager: 관리자
        ## GET
            * todos: 관리자가 처리할 글들
    """
    def get_manager(self, manager_pk, format=None):
        try:
            manager = get_object_or_404(User, pk=manager_pk)
            if manager.is_staff:
                return manager
            else:
                raise Exception
        except:
            return Response(access_message, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, manager_pk, format=None):
        manager = self.get_manager(manager_pk)
        try:
            todos = CustomersVoice.objects.filter(manager=manager_pk).order_by('-created_at')
            todo = [CustomersVoiceSerializer(t).data for t in todos]
            data = {
                'todos': todo,
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        try:
            requests = request.data
            data = {
                'title': requests.get('title'),
                'content': requests.get('content'),
                'manager': request.user,
                'is_fixed': True,
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
            * todo: 답변했던 글
    """
    def put(self, request, manager_pk, todo_pk, format=None):
        manager = get_object_or_404(User, pk=manager_pk)
        try:
            requests = request.data
            todo = get_object_or_404(CustomersVoice, pk=todo_pk)
            todo.title = requests.get['title']
            todo.content = requests.get['content']
            data = {
                'id': todo.id,
                'title': todo.title,
                'content': todo.content,
            }
            serializer = CustomersVoiceSerializer(todo, data=data)
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
        category = [NoticeCategorySerializer(c).data for c in categories]
        user = get_user(request.headers['Authorization'].split(' '))
        if user.is_staff:
            data = {
                'data': category,
            }
            return Response(data, status=status.HTTP_200_OK)
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
        notice = [NoticeSerializer(n).data for n in notices]
        data = {
            'notice': notice,
        }
        return Response(data, status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class NoticeView(APIView):
    """
        개별 공지사항 보기

        ---
    """
    def get_object(self, notice_pk, format=None):
        return get_object_or_404(Notice, pk=notice_pk)

    def get(self, request, notice_pk, format=None):
        try:
            notice = self.get_object(notice_pk)
            data = {
                'notice': NoticeSerializer(notice).data
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes((IsAuthenticated, ))
class ThemeNoticesView(APIView):
    """
        코스 공지사항 - 사용자/관리자 공통

        ---

    """
    def get_theme(self, theme_pk, format=None):
        return get_object_or_404(Theme, pk=theme_pk)
    
    def get(self, request, theme_pk, format=None):
        theme = self.get_theme(theme_pk)
        try:
            notices = theme.theme_notices.all().order_by('-writed_at')
            notice = [NoticeSerializer(n).data for n in notices]
            data = {
                'notices': notice,
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAdminUser,))
class ThemeNoticesPost(APIView):
    """
        코스 공지사항 - 관리자 화면

        ---
    """
    def post(self, request, format=None):
        try:
            requests = request.data
            data = {
                'title': requests.get('title'),
                'content': requests.get('content'),
                'writer': request.user.pk,
                'theme': requests.get('theme'),
            }
            serializer = NoticeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


class ThemeNoticesChange(APIView):
    """
        코스 공지사항 - 세부 내용(공통) | 관리자의 수정/삭제
        
        ---
    """
    def get_notices(self, notice_pk, format=None):
        return get_object_or_404(Notice, pk=notice_pk)

    @permission_classes((IsAuthenticated,))
    def get(self, request, notice_pk, format=None):
        notice = self.get_notices(notice_pk)
        serializer_n = NoticeSerializer(notice).data
        writer = serializer_n['writer']
        data = {
            'id': serializer_n['id'],
            'title': serializer_n['title'],
            'content': serializer_n['content'],
            'writer_id': writer,
            'writer_nickname': str(User.objects.get(pk=writer).nickname),            
        }
        return Response(data, status=status.HTTP_200_OK)
    
    @permission_classes((IsAdminUser,))
    def put(self, request, notice_pk, format=None):
        notice = self.get_notices(notice_pk)
        try:
            requests = request.data
            notice.title = requests.get('title')
            notice.content = requests.get('content')
            notice.writer_id = request.user.pk
            data = {
                'title': notice.title,
                'content': notice.content,
                'writer': notice.writer_id,
                'theme': requests.get('theme'),
            }
            serializer = NoticeSerializer(notice, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes((IsAdminUser,))
    def delete(self, request, notice_pk, format=None):
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
            result['theme'] = [ThemeSerializer(t_result).data for t_result in theme_results]
            result['dest'] = [DestinationSerializer(d_result).data for d_result in dest_results]
                
            return Response(result, status=status.HTTP_200_OK)
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
            comment = [CommentSerializer(c).data for c in comments]
            data = {
                'comments': comment,
            }
            return Response(data, status=status.HTTP_200_OK)
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
            recomment = [ReCommentSerializer(rc).data for rc in recomments]
            data = {
                'recomments': recomment,
            }
            return Response(data, status=status.HTTP_200_OK)
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
