from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all().order_by('owner')

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.owner != self.request.user:
            message = {'status': 'error',
                       'message': "You can't edit posts that are not yours"}
            return Response(data=message, status=status.HTTP_403_FORBIDDEN)

        return super(PostViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.owner != self.request.user:
            message = {'status': 'error',
                       'message': "You can't delete posts that are not yours"}
            return Response(data=message, status=status.HTTP_403_FORBIDDEN)

        return super(PostViewSet, self).destroy(request, *args, **kwargs)
