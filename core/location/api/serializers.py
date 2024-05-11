from rest_framework import serializers
from core.location.models import State, LGA, Region, Csp
from core.api.serializers import CustomeSerializer


class StateModelSerializer(CustomeSerializer):
   
    class Meta:
        model = State
        fields = [
            "pk",
            "title",
            "State_ID",
            "state_code",
            "zone",
            "zone_code",
            "lgas_count",
            "timestamp",
            "updated",
        ]


class StateModelComboSerializer(CustomeSerializer):
   

    class Meta:
        model = State
        fields = [
            "pk",
            "title",
            "State_ID",
            "state_code",
            "zone",
            "zone_code",
            "lgas_count",
            "get_lgas",
            "timestamp",
            "updated",
        ]

    
class LGAModelSerializer(CustomeSerializer):

    class Meta:
        model = LGA
        fields = ["pk", "title", "LGA_ID", "state", "state_title", "timestamp", "updated"]


class RegionModelSerializer(CustomeSerializer):

    class Meta:
        model = Region
        fields = [
            "pk",
            "title",
            "state",
            "state_title",
            "address",
            "cavti_id",
            "billing_prepaid_id",
            "billing_postpaid_id",
            "timestamp",
            "updated",
        ]

class CspModelSerializer(CustomeSerializer):

    class Meta:
        model = Csp
        fields = [
            "pk",
            "title",
            "region",
            "region_title",
            "address",
            "cavti_id",
            "billing_prepaid_id",
            "billing_postpaid_id",
            "timestamp",
            "updated",
        ]
