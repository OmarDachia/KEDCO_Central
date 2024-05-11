from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    MDMeterApplication,
    MDMeterApplicationTrxWindingContinutyTest,
    MDMeterApplicationTrxWindingInsulationTest
) 

# Register your models here.


@admin.register(MDMeterApplication)
class MeterApplicationAdmin(SimpleHistoryAdmin):
    list_display = (
        "uid", 
        "company_name",
        "customer", 
        "contractor", 
        # "region",
        "stage", 
        "state",
        "timestamp", "updated",
    )
    list_filter = ("timestamp", "updated", "stage", "state",)
    readonly_fields = ("uid",)
    search_fields = ("uid",)
    date_hierarchy = "timestamp"


@admin.register(MDMeterApplicationTrxWindingContinutyTest)
class MDMeterApplicationTrxWindingContinutyTestAdmin(SimpleHistoryAdmin):
    list_display = (
        "inspection",
        "application_uid",
        "timestamp", "updated",
    )
    list_filter = ("timestamp", "updated",)
    search_fields = ("inspection__uid",)
    date_hierarchy = "timestamp"

@admin.register(MDMeterApplicationTrxWindingInsulationTest)
class MDMeterApplicationTrxWindingInsulationTestAdmin(SimpleHistoryAdmin):
    list_display = (
        "inspection",
        "application_uid",
        "timestamp", "updated",
    )
    list_filter = ("timestamp", "updated",)
    search_fields = ("inspection__uid",)
    date_hierarchy = "timestamp"
