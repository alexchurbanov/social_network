from django.contrib import admin
from django.db.models import Count

from .models import Post


class AdminPost(admin.ModelAdmin):
    search_fields = ('subject', 'text')
    list_display = ('id', 'author', 'subject', 'text', 'date_published', 'last_edit', 'likes')
    list_filter = ('author', 'liked_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super(AdminPost, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_likes=Count("liked_by")
        )
        return queryset

    def likes(self, obj):
        return obj.likes

    likes.admin_order_field = 'total_likes'


admin.site.register(Post, AdminPost)
