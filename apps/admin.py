from django.contrib import admin
from .models import Application, UserAppPrivilege, Vendor
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.


@admin.register(Application)
class ApplicationAdmin(SimpleHistoryAdmin):
    list_display = ("title", "uid", "active", "timestamp", "updated",)
    list_filter = ("active", "timestamp", "updated")
    readonly_fields = ("uid",)


@admin.register(UserAppPrivilege)
class UserAppPrivilegeAdmin(SimpleHistoryAdmin):
    list_display = (
        "app",
        "profile",
        "user_type",
        "access_status",
        "timestamp",
        "updated",
        
    )
    list_filter = (
        "app",
        "profile",
        "user_type",
        "access_status",
        "timestamp",
        "updated",
    )


@admin.register(Vendor)
class VendorAdmin(SimpleHistoryAdmin):
    list_display = (
        "title",
        "uid",
        "active",
        "timestamp",
        "updated",
        
    )
    list_filter = (
        "active",
        "timestamp",
        "updated",
    )
