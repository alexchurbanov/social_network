from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.utils import timezone
from datetime import date

from .models import Post, PostAnalytics
from .serializers import PostSerializer, PostAnalyticsSerializer
from .filters import AnalyticsFilter, PostsFilter
from Accounts.functions import log_user_activity, get_client_ip


class PostViewSet(viewsets.ModelViewSet):
    """
    List of posts
    """
    serializer_class = PostSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    filterset_class = PostsFilter

    search_fields = ('text', 'subject')
    ordering_fields = ('likes', 'owner__username', 'subject', 'date_created', 'last_edit')

    def get_queryset(self):
        return Post.objects.all().order_by('-owner')

    def list(self, request, *args, **kwargs):

        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='get posts')

        return super(PostViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='create post')

        return super(PostViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='get post')
        return super(PostViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='edit post')

        if instance.owner != self.request.user:
            message = {'status': 'error',
                       'message': "You can't edit this post"}
            return Response(data=message, status=status.HTTP_403_FORBIDDEN)

        return super(PostViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='delete post')

        if instance.owner != self.request.user:
            message = {'status': 'error',
                       'message': "You can't delete this post"}
            return Response(data=message, status=status.HTTP_403_FORBIDDEN)

        return super(PostViewSet, self).destroy(request, *args, **kwargs)


class PostsAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
     Analytics about how many likes was made
    """
    serializer_class = PostAnalyticsSerializer
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    filterset_class = AnalyticsFilter

    ordering_fields = ('likes', 'date')
    queryset = PostAnalytics.objects.all().order_by('-date')

    def list(self, request, *args, **kwargs):
        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='get analytics')
        return super(PostsAnalyticsViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='get analytics')
        return super(PostsAnalyticsViewSet, self).list(request, *args, **kwargs)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def like_post(request, post_id):
    """
    Give like to a post
    """
    try:
        instance = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({
                        'id': post_id,
                        'status': 'error',
                        'message': "Post with this id doesn't exist"}, status.HTTP_404_NOT_FOUND)

    already_liked = Post.objects.filter(id=post_id, liked_by=request.user).exists()
    if not already_liked:
        instance.liked_by.add(request.user)
        instance.likes += 1
        instance.save()

        analytics = PostAnalytics.objects.get_or_create(date=date.today())
        analytics[0].likes += 1
        analytics[0].save()

        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='post like')

        return Response({
                        'id': post_id,
                        'status': 'success',
                        'message': 'Liked'}, status.HTTP_200_OK)
    else:
        return Response({
                            'id': post_id,
                            'status': 'error',
                            'message': "Post with this id already liked by you"}, status.HTTP_403_FORBIDDEN)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def unlike_post(request, post_id):
    """
    Take like from a post
    """
    try:
        instance = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({
                        'id': post_id,
                        'status': 'error',
                        'message': "Post with this id doesn't exist"}, status.HTTP_404_NOT_FOUND)
    try:
        instance = Post.objects.get(id=post_id, liked_by=request.user)
        instance.liked_by.remove(request.user)
        instance.likes -= 1
        instance.save()

        analytics = PostAnalytics.objects.get_or_create(date=date.today())
        if analytics[0].likes != 0:
            analytics[0].likes -= 1
            analytics[0].save()

        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='post unlike')

        return Response({
                        'id': post_id,
                        'status': 'success',
                        'message': 'Unliked'}, status.HTTP_200_OK)
    except Post.DoesNotExist:
        return Response({
                        'id': post_id,
                        'status': 'error',
                        'message': "Image with this id was not liked by you"},
                        status.HTTP_400_BAD_REQUEST)
