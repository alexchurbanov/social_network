from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters

from .models import Post
from .serializers import PostSerializer
from .filters import PostsFilter
from .permissions import IsPostOwnerOrAdmin


class PostViewSet(viewsets.ModelViewSet):
    """
    List of posts
    """
    permission_classes = (IsAuthenticatedOrReadOnly, IsPostOwnerOrAdmin)
    serializer_class = PostSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    filterset_class = PostsFilter

    search_fields = ('text', 'subject')
    ordering_fields = ('likes', 'author__username', 'subject', 'date_created', 'last_edit')

    def get_queryset(self):
        if self.action == 'published_posts':
            return Post.objects.filter(author=self.request.user).order_by('id')
        elif self.action == 'favourite_posts':
            return Post.objects.filter(liked_by=self.request.user).order_by('id')
        else:
            return Post.objects.all().order_by('-author')

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def like(self, request, *args, **kwargs):
        """
        Give like to a post
        """
        post = self.get_object()

        if not post.is_already_liked(request.user):
            post.liked_by.add(request.user)
            return Response({
                'id': post.id,
                'status': 'success',
                'message': 'Liked'}, status.HTTP_200_OK)
        else:
            return Response({
                'id': post.id,
                'status': 'error',
                'message': 'Post with this id already liked by you'}, status.HTTP_403_FORBIDDEN)

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def unlike(self, request, *args, **kwargs):
        """
        Take like from a post
        """
        post = self.get_object()

        if post.is_already_liked(request.user):
            post.liked_by.remove(request.user)
            return Response({
                'id': post.id,
                'status': 'success',
                'message': 'Unliked'}, status.HTTP_200_OK)
        else:
            return Response({
                'id': post.id,
                'status': 'error',
                'message': 'Post with this id was not liked by you'}, status.HTTP_403_FORBIDDEN)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def favourite_posts(self, request, *args, **kwargs):
        """
        List of liked posts
        """
        return super(PostViewSet, self).list(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def published_posts(self, request, *args, **kwargs):
        """
        List of published posts
        """
        return super(PostViewSet, self).list(request, *args, **kwargs)
