from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters import rest_framework as filters

from .models import Post, PostLikes
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

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def analytics(self, *args, **kwargs):
        """
        Analytics about how many likes were made and when
        """
        queryset = PostLikes.objects.filter(post=kwargs['pk'])
        post_likes_dates = queryset.values_list('created', flat=True)

        response = {'total_likes': post_likes_dates.count(),
                    'likes_per_day': {}}
        for date in post_likes_dates.distinct('created'):
            likes = queryset.filter(created=date).count()
            response['likes_per_day'][date.strftime("%Y-%m-%d")] = likes

        return Response(response)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def posts_analytics_view(request, *args, **kwargs):
    """
    Analytics about how many likes were made
    """
    date_from = request.query_params.get('date_from', '')
    date_to = request.query_params.get('date_to', '')
    if date_from and date_to:
        queryset = PostLikes.objects.filter(created__gte=date_from, created__lte=date_to)
    elif date_from:
        queryset = PostLikes.objects.filter(created__gte=date_from)
    elif date_to:
        queryset = PostLikes.objects.filter(created__lte=date_to)
    else:
        queryset = PostLikes.objects.all()

    dates = queryset.values_list('created', flat=True).distinct('created')

    response = []

    for date in dates:
        date_string = date.strftime("%Y-%m-%d")
        total_likes = queryset.filter(created=date).count()

        post_of_the_day = []
        most_likes = 0
        posts_likes = queryset.filter(created=date).distinct('post')
        for instance in posts_likes:
            likes = queryset.filter(post=instance.post, created=date).count()
            if likes >= most_likes:
                most_likes = likes
                post_of_the_day.append(instance.post.id)

        response.append({'date': date_string,
                         'total_likes': total_likes,
                         'top_posts': post_of_the_day})

    return Response(response)
