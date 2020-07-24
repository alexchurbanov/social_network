from django.contrib import admin
from .models import Post


class AdminPost(admin.ModelAdmin):
    search_fields = ('subject', 'text')
    list_display = ('id', 'author', 'subject', 'text', 'date_published', 'last_edit', 'likes')
    list_filter = ('author', 'liked_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super(AdminPost, self).save_model(request, obj, form, change)


admin.site.register(Post, AdminPost)
