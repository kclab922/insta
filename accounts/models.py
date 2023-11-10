from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# Create your models here.
class User(AbstractUser):
    profile_image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        upload_to='profile'
    )
    # post_set = 
    # like_posts = 

    # user끼리 연결하므로, 자기 자신을 연결하는 것
    # 대칭구조 아니야 = 1>2로 가는 것과 2>1로 가는 것을 다른 경우로 분리할거야.
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    # followers = 
 
