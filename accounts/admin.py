from django.contrib import admin
from .models import (
    UserProfile, UserType,
    CustomerProfile, VendorProfile,
    ContractorProfile,
    PasswordResetTokens,

)
from simple_history.admin import SimpleHistoryAdmin


# Register your models here


@admin.register(UserProfile)
class UserProfileAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "fullname",
        "staff_id",
        "get_email",
        "phone_number",
        "region",
        "csp",
        "get_last_login",
        "active",
        "timestamp",
        "updated",
    )
    list_filter = ("active", "timestamp", "updated",
                   "region", "csp")
    autocomplete_fields = ["user"]
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "phone_number", "staff_id")
    date_hierarchy = "timestamp"


@admin.register(CustomerProfile)
class CustomerProfileAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "fullname",
        "get_email",
        "phone_number",
        "region",
        "get_last_login",
        "active",
        "timestamp",
        "updated",
    )
    list_filter = ("active", "timestamp", "updated", )
    autocomplete_fields = ["user"]
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "phone_number",)
    date_hierarchy = "timestamp"
    


@admin.register(UserType)
class UserTypeAdmin(SimpleHistoryAdmin):
    list_display = ("title", "uid", "status", "timestamp", "updated", )
    list_filter = ("status", "timestamp", "updated", )


@admin.register(VendorProfile)
class VendorProfileAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "fullname",
        "get_email",
        "phone_number",
        "vendor",
        "get_last_login",
        "active",
        "timestamp",
        "updated",
    )
    list_filter = ("active", "timestamp", "updated", )
    autocomplete_fields = ["user"]
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email", "phone_number",)
    date_hierarchy = "timestamp"


@admin.register(ContractorProfile)
class ContractorProfileAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "fullname",
        "get_email",
        "phone_number",
        "company_name",
        "nemsa_licence",
        "get_last_login",
        "active",
        "timestamp",
        "updated",
    )
    list_filter = ("active", "timestamp", "updated", )
    autocomplete_fields = ["user"]
    search_fields = ("user__username", "user__first_name",
                     "user__last_name", "user__email", "phone_number", "nemsa_licence",
                    )
    date_hierarchy = "timestamp"
    readonly_fields = ("uid",)


@admin.register(PasswordResetTokens)
class PasswordResetTokensAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "fullname",
        "get_email",
        "sent_count",
        "active",
        "timestamp",
        "updated",
    )
    list_filter = ("active", "timestamp", "updated", )
    autocomplete_fields = ["user"]

