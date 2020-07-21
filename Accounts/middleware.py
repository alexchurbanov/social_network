from django.utils.timezone import now
from .models import User
from .functions import get_client_ip


class LastRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.user.is_authenticated:
            User.objects.filter(id=request.user.id).update(last_request=now(),
                                                           last_IP=get_client_ip(request))
        return response
