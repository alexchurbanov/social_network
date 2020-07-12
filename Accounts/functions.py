from .models import UserLastActivity


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_user_activity(user, **kwargs):
    if user.is_authenticated:
        UserLastActivity.objects.update_or_create(user=user, defaults=kwargs)
