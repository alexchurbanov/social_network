from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import User
from .functions import log_user_activity, get_client_ip


@receiver(user_logged_in)
def on_login(sender, user, request, **kwargs):
    timestamp = timezone.now()
    log_user_activity(user, last_login=timestamp,
                      last_request_IP=get_client_ip(request),
                      last_request=timestamp, last_request_type='login')


@receiver(user_logged_out)
def on_logout(sender, user, request, **kwargs):
    timestamp = timezone.now()
    log_user_activity(user, last_request_IP=get_client_ip(request),
                      last_request=timestamp, last_request_type='logout')


@receiver(post_save, sender=User)
def on_user_create(sender, instance, **kwargs):
    timestamp = timezone.now()
    log_user_activity(instance, last_request=timestamp, last_request_type='signUp')