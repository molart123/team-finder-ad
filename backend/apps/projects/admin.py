from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description', 'owner__email', 'owner__name', 'owner__surname')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {'fields': ('name', 'description', 'owner', 'github_url', 'status')}),
        (_('Participants'), {'fields': ('participants',)}),
        (_('Timestamps'), {'fields': ('created_at',)}),
    )
    filter_horizontal = ('participants',)