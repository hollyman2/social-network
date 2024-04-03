import uuid
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


Account = get_user_model()

    
class Post(models.Model):
    VIDEO_VALIDATOR = FileExtensionValidator(allowed_extensions=['mp4', ])

    id = models.UUIDField(
        'UUID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    tags = models.CharField(
        'Tags',
        max_length=100,
        default=''
    )
    picture = models.ImageField(
        'Picture',
        upload_to='posts_pictures/%Y/%m/%d/',
        null=True,
        blank=True
    )
    video = models.FileField(
        'Video',
        upload_to='posts_videos/images/%Y/%m/%d/',
        null=True,
        blank=True,
        validators=[VIDEO_VALIDATOR, ]
    )
    description = models.TextField(
        'Description',
        max_length=500,
    )
    count_of_likes = models.IntegerField(
        'Count of likes',
        default=0
    )
    author = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='get_posts',
        verbose_name='Author'
    )
    date_created = models.DateTimeField(
        'Date created',
        auto_now_add=True
    )

    def __str__(self):
        return self.description[:50]

    def get_absolute_url(self):
        return reverse(
            'profile_detail',
            args=[str(self.id)]
        )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='get_comments',
        verbose_name='Post'
    )
    author = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='get_user_comments',
        verbose_name='Author'
    )
    description = models.TextField(
        'Description',
        max_length=500,
    )
    count_of_likes = models.IntegerField(
        'Count of likes',
        default=0
    )
    edited = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.description[:50]

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class ReplyComment(Comment):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='get_reply_comment'
    )

    def __str__(self):
        return self.comment.description[:50]

    class Meta:
        verbose_name = 'Reply to comment'
        verbose_name_plural = 'Replies to comment'


class Like(models.Model):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='get_user_likes',
        verbose_name='User'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='get_post_likes',
        verbose_name='Liked post',
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='get_comment_likes',
        verbose_name='Liked comment',
        null=True,
        blank=True
    )
    reply_comment = models.ForeignKey(
        ReplyComment,
        on_delete=models.CASCADE,
        related_name='get_reply_comment_likes',
        verbose_name='Liked reply comment',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username

    

class Report(models.Model):
    author = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='report_creator',
        verbose_name='Report author'
    )
    recipient = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='report_recipient',
        verbose_name='Report recipient',
        null=True,
        blank=True
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='report_post',
        verbose_name='Report post',
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='report_comment',
        verbose_name='Report comment',
        null=True,
        blank=True
    )
    answer = models.ForeignKey(
        ReplyComment,
        on_delete=models.CASCADE,
        related_name='report_answer',
        verbose_name='Report answer',
        null=True,
        blank=True
    )
    reason = models.CharField(
        'Reason',
        max_length=255
    )
    created = models.DateTimeField(auto_now_add=True)
