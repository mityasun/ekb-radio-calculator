from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from rest_framework import status


@ratelimit(key='ip', rate='3/m', method='POST', block=True)
def custom_admin_login(request, *args, **kwargs):
    from django.contrib.admin.sites import AdminSite
    return AdminSite().login(request, *args, **kwargs)


def view_404(request, exception=None):
    """View return 404 page for all non exist pages."""

    return HttpResponseRedirect('/404')


def view_429(request, exception):
    """View for 429 too many requests."""

    return JsonResponse(
        {'error': 'Too many requests, please try again later.'},
        status=status.HTTP_429_TOO_MANY_REQUESTS
    )
