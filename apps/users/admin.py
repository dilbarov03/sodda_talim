from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
        ("Login details", {'fields': ('phone', 'password', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                        'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
            (_('User info'), {'fields': ('first_name', 'last_name', 'image')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('phone', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    list_display = ['phone', 'first_name', 'last_name', 'is_staff',  "phone"]
    search_fields = ('phone', 'first_name', 'last_name')
    ordering = ('phone', )


admin.site.register(User, UserAdmin)
