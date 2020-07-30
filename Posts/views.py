from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters import rest_framework as filters

from .models import Post, PostLikes
from .serializers import PostSerializer
from .filters import PostsFilter, DateRangePostLikesFilter
from .permissions import IsPostOwnerOrAdmin


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD operations with posts
    """
    permission_classes = (IsAuthenticatedOrReadOnly, IsPostOwnerOrAdmin)
    serializer_class = PostSerializer
    filter_backends = (SearchFilter, OrderingFilter, filters.DjangoFilterBackend)
    filterset_class = PostsFilter

    search_fields = ('text', 'subject')
    ordering_fields = ('author__username', 'date_published')

    def get_queryset(self):
        if self.action == 'published_posts':
            return Post.objects.filter(author=self.request.user).order_by('date_published')
        elif self.action == 'favourite_posts':
            return Post.objects.filter(liked_by=self.request.user).order_by('date_published')
        else:
            return Post.objects.all().order_by('author')

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

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny],
            filter_backends=[DateRangePostLikesFilter])
    def analytics(self, request, pk, *args, **kwargs):
        """
        Analytics about how many likes were made to this post
        """
        queryset = self.filter_queryset(PostLikes.objects.filter(post__id=pk))

        response = []

        dates = queryset.values_list('created', flat=True)
        for date in dates.distinct('created'):
            likes = queryset.filter(created=date).count()
            date_string = date.strftime("%Y-%m-%d")
            response.append({'date': date_string,
                             'likes': likes})

        page = self.paginate_queryset(response)
        if page is not None:
            return self.get_paginated_response(page)


class PostAnalyticsViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin):
    """
    Analytics about how many likes were made
    """
    permission_classes = [AllowAny]
    filter_backends = [DateRangePostLikesFilter]
    queryset = PostLikes.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset)
        dates = queryset.values_list('created', flat=True).distinct('created')

        response = []

        for date in dates:
            date_string = date.strftime("%Y-%m-%d")
            total_likes = queryset.filter(created=date).count()

            top_posts = []
            most_likes = 0
            posts_likes = queryset.filter(created=date).distinct('post')
            for instance in posts_likes:
                likes = queryset.filter(post=instance.post, created=date).count()
                if likes >= most_likes:
                    if most_likes == likes:
                        top_posts.append(instance.post.id)
                    else:
                        most_likes = likes
                        top_posts = [instance.post.id]

            response.append({'date': date_string,
                             'total_likes': total_likes,
                             'most_likes': most_likes,
                             'top_posts': top_posts})

        page = self.paginate_queryset(response)
        if page is not None:
            return self.get_paginated_response(page)
        return Response(response)
