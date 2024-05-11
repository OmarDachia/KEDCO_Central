from core.api.serializers import CustomeSerializer

from ami.models import (
    Device,
    DeviceReading,
)


class DeviceDetailsSerializer(CustomeSerializer):
    class Meta:
        model = Device
        fields = [
            "pk",
            "uid",
            "meter_number",
            "device_pk",
            "feeder_33",
            "feeder_33_title",
            "feeder_11",
            "feeder_11_title",
            "voltage_level",
            "transmission_station",
            "transmission_station_title",
            "injection_substation",
            "injection_substation_title",
            "band",
            "commissioned_date",
            "timestamp",
            "updated",
            "audits",
            "revisions",
        ]
        

class DeviceListSerializer(CustomeSerializer):
    class Meta:
        model = Device
        fields = [
            "pk",
            "uid",
            "meter_number",
            "device_pk",
            "feeder_33",
            "feeder_33_title",
            "feeder_11",
            "feeder_11_title",
            "voltage_level",
            "transmission_station",
            "transmission_station_title",
            "injection_substation",
            "injection_substation_title",
            "band",
            "commissioned_date",
            "timestamp",
            "updated",
        ]
        
#
class DeviceReadingDetailsSerializer(CustomeSerializer):
    class Meta:
        model = DeviceReading
        fields = [
            "pk",
            "uid",
            "meter",
            "meter_number",
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
            "timestamp",
            "updated",
            "audits",
            "revisions",
        ]

class DeviceReadingListSerializer(CustomeSerializer):
    class Meta:
        model = DeviceReading
        fields = [
            "pk",
            "uid",
            "meter",
            "meter_number",
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
            "timestamp",
            "updated",
        ]