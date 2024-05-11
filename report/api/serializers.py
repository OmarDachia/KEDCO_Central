from rest_framework import serializers
from core.api.serializers import CustomeSerializer

from nmmp.models import (
    NMMPKYC,
)


class NMMPKYCDetailsSerializer(CustomeSerializer):
    kyc_by = serializers.SerializerMethodField()

    class Meta:
        model = NMMPKYC
        fields = [
            "pk",
            "uid",
            "first_name",
            "other_name",
            "last_name",
            "phone_number",
            "email",
            "region",
            "region_title",
            "csp",
            "csp_title",
            "address",
            "band",
            # "customer",
            # "customer_name",
            "account_number",
            "bookcode",
            "meter_number",
            "meter_phase",
            "meter_phase_title",
            "feeder",
            "feeder_title",
            "transformer",
            "transformer_title",
            "kyc_by",
            "kyc_by_staff",
            "longitude",
            "latitude",
            "altitude",
            "accuracy",
            "audits",
            "stage",
            "timestamp",
            "updated",
        ]

    def get_kyc_by(self, obj):
        return f"{obj.kyc_by.pk}"
