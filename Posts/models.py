from django.db import models
from SocialNetwork.settings import AUTH_USER_MODEL
import uuid


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, related_name='user')
    subject = models.CharField(max_length=50)
    text = models.TextField(max_length=300)
    date_published = models.DateTimeField(auto_now_add=True, editable=False)
    last_edit = models.DateTimeField(auto_now=True, editable=False)
    liked_by = models.ManyToManyField(AUTH_USER_MODEL, through='PostLikes', related_name='post_likes')

    def __str__(self):
        return str(self.id)

    @property
    def likes(self):
        return self.liked_by.count()

    def is_already_liked(self, user):
        return PostLikes.objects.filter(post=self.id, user=user).exists()

    class Meta:
        db_table = 'Posts'


class PostLikes(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Posts_likes'
        unique_together = ('user', 'post')
