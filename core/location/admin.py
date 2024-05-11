from django.contrib import admin
from .models import State, LGA, Region, Csp
from simple_history.admin import SimpleHistoryAdmin


@admin.register(LGA)
class LGAAdmin(SimpleHistoryAdmin):
    list_display = ["title", "LGA_ID", "state", "timestamp", "updated"]
    search_fields = ["title", "LGA_ID", "state__title"]
    list_filter = ["timestamp", "updated", "state"]


@admin.register(State)
class StateAdmin(SimpleHistoryAdmin):
    list_display = ["title", "state_code",
                    "lgas_count", "timestamp", "updated"]
    search_fields = [
        "title", "State_ID", "state_code", "zone_code",
    ]
    list_filter = ["timestamp", "updated", "zone", "zone_code"]


@admin.register(Region)
class RegionAdmin(SimpleHistoryAdmin):
    list_display = [
        "title", "state", 
        "cavti_id", "billing_prepaid_id", "billing_postpaid_id",
        "timestamp", "updated"
    ]
    search_fields = [
        "title", "address",
        "cavti_id", "billing_prepaid_id", "billing_postpaid_id",
    ]
    list_filter = ["timestamp", "updated", "state",]


@admin.register(Csp)
class CspAdmin(SimpleHistoryAdmin):
    list_display = [
        "title", "region", "lga", 
        "cavti_id", "billing_prepaid_id", "billing_postpaid_id",
        "timestamp", "updated"
    ]
    search_fields = [
        "title", "address", 
        "cavti_id", "billing_prepaid_id", "billing_postpaid_id",
    ]
    list_filter = ["timestamp", "updated", "region", "region__state"]
