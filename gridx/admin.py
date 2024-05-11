from django.contrib import admin
from .models import Feeder, Station, Transformer, TransmissionStation
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.


@admin.register(Feeder)
class FeederAdmin(SimpleHistoryAdmin):
    list_display = (
        "title", "code", "band", "transformer_count",
        "capacity", "parent_feeder", 
        "cavti_id", "billing_prepaid_id", "billing_postpaid_id",
        "timestamp", "updated",
        )
    list_filter = (
        "timestamp", "updated", 
        "capacity",
        "band", 
        # "parent_feeder",
        "region",
        )
    # readonly_fields = ("uid",)
    search_fields = (
        "title", "code",
        "cavti_id", "billing_prepaid_id", "billing_postpaid_id",
    )

@admin.register(Transformer)
class TransformerAdmin(SimpleHistoryAdmin):
    list_display = (
        "title", "code", "feeder", "csp",
        "cavti_id", "billing_prepaid_id", "billing_postpaid_id",
        "timestamp", "updated",
    )
    list_filter = (
        "timestamp", "updated",
        "feeder",
    )
    search_fields = (
        "title", "code",
        "bookcode_1", "bookcode_2", "bookcode_3"
        "cavti_id", "billing_prepaid_id", "billing_postpaid_id",
    )

@admin.register(TransmissionStation)
class TransmissionStationAdmin(SimpleHistoryAdmin):
    list_display = ("title", "cavti_id", "state", "timestamp", "updated",)
    search_fields = ("title", )

@admin.register(Station)
class StationAdmin(SimpleHistoryAdmin):
    list_display = ("title", "code", "capacity", "transmission", "region", "cavti_id", "timestamp", "updated",)
    search_fields = ("title", )





