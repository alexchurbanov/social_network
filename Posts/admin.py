from django.contrib import admin
from .models import Post


class AdminPost(admin.ModelAdmin):
    search_fields = ('subject', 'text')
    list_display = ('id', 'owner', 'subject', 'text', 'date_published', 'last_edit', 'likes')
    list_filter = ('subject', 'owner', 'liked_by')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super(AdminPost, self).save_model(request, obj, form, change)


class AdminPostAnalytics(admin.ModelAdmin):
    list_display = ('date', 'likes')
    readonly_fields = ('date', 'likes')


admin.site.register(Post, AdminPost)
