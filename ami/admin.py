from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin


from .models import (
    Device,
    DeviceReading,
)
# Register your models here.

@admin.register(Device)
class DeviceAdmin(SimpleHistoryAdmin):
    list_display = (
        "uid",
        "meter_number",
        "device_pk",
        "feeder_33",
        "feeder_11",
        "transmission_station",
        "injection_substation",
        "band",
        "timestamp", "updated",
    )
    list_filter = ("timestamp", "updated",)
    search_fields = ("uid", "meter_number",)
    date_hierarchy = "timestamp"
    readonly_fields = ("uid", "timestamp", "updated",)
    autocomplete_fields = ("feeder_33", "feeder_11", "transmission_station", "injection_substation")

@admin.register(DeviceReading)
class DeviceReadingAdmin(SimpleHistoryAdmin):
    list_display = (
        "meter",
        "reading_timestamp",
        "VA",
        "VB",
        "VC",
        "IA",
        "IB",
        "IC",
        "PF",
        "MW",
        "MW2",
        "date",
        "time",
        "timestamp", "updated",
    )
    list_filter = ("timestamp", "updated",)
    search_fields = ("meter__uid", "meter__meter_number",)
    date_hierarchy = "timestamp"
    readonly_fields = ("timestamp", "updated",)
    autocomplete_fields = ("meter", )
