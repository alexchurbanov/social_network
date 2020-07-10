from django.db import models
from SocialNetwork.settings import AUTH_USER_MODEL
from django.utils import timezone
import uuid


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False, related_name='owner')
    subject = models.CharField(max_length=50)
    text = models.TextField(max_length=200)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    likes = models.IntegerField(default=0, editable=False)
    liked_by = models.ManyToManyField(AUTH_USER_MODEL, blank=True, editable=False, related_name='liked_by')

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'Posts'
