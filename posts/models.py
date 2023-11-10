from django.db import models
from django_resized import ResizedImageField
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
class Post(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # image = models.ImageField(upload_to='image/%Y/%m')
    image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='image/%Y/%m'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # related_name => Post와 User를 연결하는 과정에서 1:N, M:N으로 두 번 연결됨
    # => User 쪽에 자동생성되는 post_set도 2개가 만들어짐 -> 이름 중복되므로 하나 변경
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_posts')

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)