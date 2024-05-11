from django.contrib import admin
from .models import (
    MeterApplication, MeterApplicationKYC, 
    MeterApplicationInstallation, MeterPhase,
    MeterApplicationPayment,
)
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
@admin.register(MeterApplication)
class MeterApplicationAdmin(SimpleHistoryAdmin):
    list_display = ("uid", "customer", "region", "stage", "timestamp", "updated",)
    list_filter = ("timestamp", "updated", "stage", "region",)
    readonly_fields = ("uid",)
    search_fields = ("uid",)
    date_hierarchy = "timestamp"


@admin.register(MeterApplicationKYC)
class MeterApplicationKYCAdmin(SimpleHistoryAdmin):
    list_display = ("application", "region", "csp",
                    "account_number",
                    "meter_number", "kyc_by", 
                    "timestamp", "updated",
                )
    list_filter = ("timestamp", "updated", "region", "band", "kyc_by")
    # readonly_fields = ("uid",)
    search_fields = ("application__uid",)
    date_hierarchy = "timestamp"


@admin.register(MeterApplicationInstallation)
class MeterApplicationInstallationAdmin(SimpleHistoryAdmin):
    list_display = ("application",
                    "meter_number", "installed_by",
                    "timestamp", "updated",
                )
    list_filter = ("timestamp", "updated",)
    # readonly_fields = ("uid",)
    search_fields = ("application__uid",)
    date_hierarchy = "timestamp"


@admin.register(MeterPhase)
class MeterPhaseAdmin(SimpleHistoryAdmin):
    list_display = ("phase", "price", "timestamp", "updated",)
    list_filter = ("timestamp", "updated",)
    # readonly_fields = ("uid",)
    search_fields = ("phase", "price")


@admin.register(MeterApplicationPayment)
class MeterApplicationPaymentAdmin(SimpleHistoryAdmin):
    list_display = (
        "application",
        "amount", 
        "payment_date",
        "approved_by",
        "timestamp", "updated",
    )
    list_filter = ("timestamp", "updated",)
    # readonly_fields = ("uid",)
    search_fields = ("application__uid",)
    date_hierarchy = "timestamp"
