from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import UserLastActivity


class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    list_display = ('id', 'email', 'username', 'is_staff', 'is_superuser',
                    'is_active', 'date_joined')
    readonly_fields = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    search_fields = ('id', 'username', 'email')
    ordering = ('email',)


class AdminUserActivities(admin.ModelAdmin, ):
    model = UserLastActivity
    list_display = ('user', 'last_login', 'last_request', 'last_request_type', 'last_request_IP')
    readonly_fields = ('user', 'last_login', 'last_request', 'last_request_type', 'last_request_IP')
    list_filter = ('user',)
    search_fields = ('user__username', 'last_login', 'last_request', 'last_request_type', 'last_request_IP')


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(UserLastActivity, AdminUserActivities)
