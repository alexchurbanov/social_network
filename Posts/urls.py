from django.urls import path
from .views import like_post, unlike_post

urlpatterns = [
    path('<uuid:post_id>/like/', like_post, name='like_post'),
    path('<uuid:post_id>/unlike/', unlike_post, name='unlike_post'),
]
