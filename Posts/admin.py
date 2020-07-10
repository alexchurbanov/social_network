from django.contrib import admin
from .models import Post


class AdminPost(admin.ModelAdmin):
    search_fields = ('id', 'subject', 'owner__email', 'text')
    list_display = ('id', 'subject', 'text', 'owner')
    list_filter = ('subject', 'owner')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super(AdminPost, self).save_model(request, obj, form, change)


admin.site.register(Post, AdminPost)
