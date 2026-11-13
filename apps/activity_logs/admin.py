from django.contrib import admin
from .models import ActivityLog

# Register your models here.
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'log_type',
        'severity',
        'ip_address',
        'created_at',
    )

    list_filter = (
        'log_type',
        'severity',
        'created_at',
    )

    search_fields = (
        'user__username',
        'message',
        'ip_address',
    )

    ordering = ('-created_at',)
