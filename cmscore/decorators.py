from django.http import HttpResponseForbidden
from functools import wraps

def secretariat_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.secretariat:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to view this page.")
    return _wrapped_view