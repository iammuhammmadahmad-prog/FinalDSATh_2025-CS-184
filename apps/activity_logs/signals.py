
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

from .models import ActivityLog


def get_client_ip(request):
    if request is None:
        return None

    return request.META.get('REMOTE_ADDR')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):

    ActivityLog.objects.create(
        user=user,
        log_type='LOGIN',
        severity='INFO',
        message=f'{user.username} logged in successfully.',
        ip_address=get_client_ip(request)
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):

    if user is None:
        return

    ActivityLog.objects.create(
        user=user,
        log_type='LOGOUT',
        severity='INFO',
        message=f'{user.username} logged out.',
        ip_address=get_client_ip(request)
    )


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):

    username = credentials.get('username', 'Unknown')

    ActivityLog.objects.create(
        user=None,
        log_type='FAILED_LOGIN',
        severity='WARNING',
        message=f'Failed login attempt for username: {username}',
        ip_address=get_client_ip(request)
    )
