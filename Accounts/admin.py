from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    list_display = ('id', 'email', 'username', 'is_staff', 'is_superuser',
                    'is_active')
    readonly_fields = ('date_joined', 'last_login',
                       'last_request', 'last_IP',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('date_joined',)}),
        ('Last Activity', {'fields': ('last_login', 'last_request', 'last_IP')})
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


admin.site.register(get_user_model(), CustomUserAdmin)
