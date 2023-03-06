from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = (
        "pk",
        "username",
        "phone",
        "email",
        "role"
    )
    search_fields = (
        "pk",
        "phone",
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
