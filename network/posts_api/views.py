from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from .models import Like, Comment, Post, ReplyComment
from rest_framework.views import APIView
from .models import Post, Comment, ReplyComment
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from .models import Report


User = get_user_model()

        
class LikeAPIView(APIView):
    def post(self, request, *args, **kwargs):

        user = request.user

        object_id = request.data.get('object_id')
        object_type = request.data.get('object_type')

        if object_type == 'post':
            obj = get_object_or_404(Post, id=object_id)
            like, created = Like.objects.get_or_create(user=user, post=obj)
        elif object_type == 'comment':
            obj = get_object_or_404(Comment, id=object_id)
            like, created = Like.objects.get_or_create(user=user, comment=obj)
        elif object_type == 'reply_comment':
            obj = get_object_or_404(ReplyComment, id=object_id)
            like, created = Like.objects.get_or_create(user=user, reply_comment=obj)
        else:
            return Response({'error': 'Invalid object type'}, status=status.HTTP_400_BAD_REQUEST)

        if not created:
            like.delete()
            return Response(
                {'message': 'Лайк был удален'},
                status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'message': 'Лайк был добавлен'},
            status=status.HTTP_201_CREATED
        )

class PostsListView(APIView):

    def get(self, request):
        post = get_list_or_404(Post)
        post_serializer = serializers.PostSerializer(post, many=True)
        return Response(
            {'post': post_serializer.data},
            status=status.HTTP_200_OK
        )


class PostDetailView(APIView):

    def get(self, request, id):

        post = get_object_or_404(Post, id=id)
        post_serializer = serializers.PostSerializer(post)
        try:
            comments = get_list_or_404(Comment, post=post)
            comment_serializer = serializers.CommentSerializer(comments, many=True)
            data = comment_serializer.data
        except:
            data = None
        
        return Response(
            {'post': post_serializer.data,
            'comments': data},
            status=status.HTTP_200_OK
        )
    
    def patch(self, request, id):
        user = request.user
        post = get_object_or_404(Post, id=id)
        serializer = serializers.PostSerializer(post)
        if user.id == serializer.data.get('author'):
            serializer = serializers.PostSerializer(
                serializer.edit(
                    data=request.data,
                    post=post
                )
            )
            return Response(
                {'post': serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'You are not the owner'}
            )
        
    def delete(self, request, id):

        user = request.user
        post = get_object_or_404(Post, id=id)
        post_serializer = serializers.PostSerializer(post)
        if user.id == post_serializer.data.get('author'):
            post.delete()
            return Response(
                {'message': 'The post has been deleted'},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {'error': 'You are not the owner'}
            )


class CreatePostView(APIView):

    def post(self, request):

        user = request.user
        serializer = serializers.PostSerializer()
        
        serializer = serializers.PostSerializer(
            serializer.create(
                request.data,
                user=user
            )
        )

        return Response(
            {'post': serializer.data},
            status=status.HTTP_201_CREATED
        )
        


class CreateCommentView(APIView):

    def post(self, request, id):
        user = request.user
        post = get_object_or_404(Post, id=id)
        serializer = serializers.CommentSerializer()
        
    
        serializer = serializers.CommentSerializer(
            serializer.create(
                data=request.data,
                user=user,
                post=post
            )
        )

        return Response(
            {'comment': serializer.data},
            status=status.HTTP_201_CREATED
           )


class DetailCommentView(APIView):

    def get(self, request, id, commentid):

        comment = get_object_or_404(Comment, id=commentid)
        comment_serializer = serializers.CommentSerializer(comment)
        try:
            answers = get_list_or_404(ReplyComment, comment=comment)
            answers_serializer = serializers.AnswerSerializer(answers, many=True)
            data = answers_serializer.data
        except:
            data = None
        return Response(
            {'comments': comment_serializer.data,
             'answers': data},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, id, commentid):
        user = request.user
        comment = get_object_or_404(Comment, id=commentid)
        comment_serializer = serializers.CommentSerializer(comment)
        if user.id == comment_serializer.data.get('author'):
            comment.delete()

            return Response(
                {'message': 'The comment has been deleted'},
                status=status.HTTP_200_OK,

            )
        else:

            return Response(
                {'error': 'You are not the owner'}
            )

    def patch(self, request, id, commentid):
        user = request.user
        comment = get_object_or_404(Comment, id=commentid)
        serializer = serializers.CommentSerializer(comment)
        if user.id == serializer.data.get('author'):

            serializer = serializers.CommentSerializer(
                serializer.edit(
                    data=request.data,
                    comment=comment
                )
            )

            return Response(
                {'comment': serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'You are not the owner'}
            ) 
class CreateAnswerView(APIView):

    def post(self, request, id, commentid):
        user = request.user
        post = get_object_or_404(Post, id=id)
        comment = get_object_or_404(Comment, id=commentid)
      
        serializer = serializers.AnswerSerializer()
        serializer = serializers.AnswerSerializer(
            serializer.create(
                data=request.data,
                user=user,
                comment=comment,
                post=post
            )
        )
        
        return Response(
            {
                'answer': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class  DetailAnswerView(APIView):
    def get(self, request, id, commentid, answerid):
       
        answer = get_object_or_404(ReplyComment, id=answerid)
        answer_serializer = serializers.AnswerSerializer(answer)

        return Response(
                {'answer': answer_serializer.data},
                status = status.HTTP_200_OK
            )
    def delete(self, request, id, commentid, answerid):
        user = request.user
        answer = get_object_or_404(ReplyComment, id=answerid)
        answer_serializer = serializers.AnswerSerializer(answer)
        if user.id == answer_serializer.data.get('author'):
            answer.delete()

            return Response(
                {'message': 'The answer has been deleted'},
                status = status.HTTP_200_OK
            )
        else:

            return Response(
                {'error': 'You are not the owner'}
            )
    def patch(self, request, id, commentid, answerid):
        user = request.user
        answer = get_object_or_404(ReplyComment, id=answerid)
        answer_serializer = serializers.AnswerSerializer(answer)
        if user.id == answer_serializer.data.get('author'):
            serializer = serializers.AnswerSerializer()
            serializer = serializers.AnswerSerializer(
                serializer.edit(
                    data=request.data,
                    answer=answer
                )
            )

            return Response(
                {'answer': serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'You are not the owner'}
            )
    

class ReportPostView(APIView):
    def post(self, request, id):

        author = request.user
        post = get_object_or_404(Post, id=id)
        post_serializer = serializers.PostSerializer(post)  
        
        try:
            report = get_object_or_404(Report, post=post, author=author)
            
            return Response(
                    {'message': 'Вы уже оправили жалобу на данный пост'}
                )
        except:

            if author.id == post_serializer.data.get('author'):

                return Response(
                        {'message': 'Вы не можете отправлять жалобу на свой пост'}
                    )
    
            report = Report.objects.create(
                author=author,
                post=post,
                reason=request.data.get('reason'),
            )
            serializer = serializers.ReportSerializer(report)



            return Response(
                    {'report': serializer.data},
                    status=status.HTTP_201_CREATED
                )
        
class ReportCommentView(APIView):
    def post(self, request, id, commentid):
        author = request.user
        comment = get_object_or_404(Comment, id=commentid)   
        comment_serializer = serializers.CommentSerializer(comment)  

        try:
            report = get_object_or_404(Report, comment=comment, author=author)
            return Response(
                    {'message': 'Вы уже оправили жалобу на данный комментарий'}
                )
        except:
            if author.id == comment_serializer.data.get('author'):
                return Response(
                        {'message': 'Вы не можете отправлять жалобу на свой ответ'}
                    )
            report = Report.objects.create(
                author=author,
                comment=comment,
                reason=request.data.get('reason'),
            )
            serializer = serializers.ReportSerializer(report)
            
            

            return Response(
                    {'report': serializer.data},
                    status=status.HTTP_201_CREATED
                )
    
class ReportAnswerView(APIView):
    def post(self, request, id, commentid, answerid):
        author = request.user
        answer = get_object_or_404(ReplyComment, id=answerid)
        answer_serializer = serializers.AnswerSerializer(answer)  
        print('rge')
        try:
            report = get_object_or_404(Report, answer=answer, author=author)
            return Response(
                    {'message': 'Вы уже оправили жалобу на данный ответ на комментарий'}
                )
        except:
            if author.id == answer_serializer.data.get('author'):
                return Response(
                        {'message': 'Вы не можете отправлять жалобу на свой ответ'}
                    )
            report = Report.objects.create(
                author=author,
                answer=answer,
                reason=request.data.get('reason'),
            )
            serializer = serializers.ReportSerializer(report)
            
            

            return Response(
                    {'report': serializer.data},
                    status=status.HTTP_201_CREATED
                )