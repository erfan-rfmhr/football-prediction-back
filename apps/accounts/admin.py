from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Gathering

admin.site.register(User, UserAdmin)

@admin.register(Gathering)
class GatheringAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'owner',)
    search_fields = ('name', 'code', 'owner__username')
    raw_id_fields = ('owner',)
    filter_horizontal = ('members',)
