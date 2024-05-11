from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import NMMPKYC, NMMPMeter, NMMPMeterInstallation, NMMPMeterUpload, NMMPApplicationType
# Register your models here.


@admin.register(NMMPKYC)
class NMMPKYCAdmin(SimpleHistoryAdmin):
    list_display = (
        "uid",
        "first_name",
        # "other_name",
        "last_name",
        "region", "csp",
        "account_number",
        # "meter_number", 
        "kyc_by",
        "timestamp", "updated",
    )
    list_filter = ("timestamp", "updated", "region", "application_type")
    readonly_fields = ("uid",)
    search_fields = (
        "first_name", "other_name", "last_name",
        "account_number", "meter_number",
        "address",
    )
    date_hierarchy = "timestamp"


@admin.register(NMMPMeterUpload)
class NMMPMeterUploadAdmin(SimpleHistoryAdmin):
    list_display = (
        "vendor",
        "upload_by",
        "meter_phase",
        "timestamp", "updated",
    )
    list_filter = ("timestamp", "updated", "vendor", "meter_phase")
    # readonly_fields = ("uid",)
    autocomplete_fields = ("upload_by", "meter_phase")
    search_fields = (
        "vendor__title", 
        # "upload_by"
    )
    date_hierarchy = "timestamp"

@admin.register(NMMPMeter)
class NMMPMeterAdmin(SimpleHistoryAdmin):
    list_display = (
        "vendor",
        "meter_number",
        "carton_number",
        "SGC",
        "FPU",
        "assigned",
        "timestamp", "updated",
    )
    list_filter = ("assigned", "timestamp", "updated", "vendor",)
    # readonly_fields = ("uid",)
    search_fields = (
        "vendor__title", "meter_number"
    )
    date_hierarchy = "timestamp"


@admin.register(NMMPMeterInstallation)
class NMMPMeterInstallationAdmin(SimpleHistoryAdmin):
    list_display = (
        "kyc",
        "meter_number", "installed_by",
        "timestamp", "updated",
    )
    list_filter = ("timestamp", "updated",)
    # readonly_fields = ("uid",)
    search_fields = ("kyc__uid",)
    date_hierarchy = "timestamp"


@admin.register(NMMPApplicationType)
class NMMPApplicationTypeAdmin(SimpleHistoryAdmin):
    list_display = (
        "title", "status",
        "timestamp", "updated",
    )
    list_filter = ("timestamp", "updated",)
    # readonly_fields = ("uid",)
    search_fields = ("title",)
    date_hierarchy = "timestamp"
