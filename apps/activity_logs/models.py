from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ActivityLog(models.Model):

    LOG_TYPES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('SIGNUP', 'Signup'),
        ('FAILED_LOGIN', 'Failed Login'),
        ('ERROR', 'Error'),
    ]

    SEVERITY_LEVELS = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('CRITICAL', 'Critical'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    log_type = models.CharField(
        max_length=20,
        choices=LOG_TYPES
    )

    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_LEVELS,
        default='INFO'
    )

    message = models.TextField()

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.log_type} - {self.message}"
