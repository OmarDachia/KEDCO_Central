from rest_framework import serializers
from core.api.serializers import CustomeSerializer

from meters.models import (
    MeterApplication, MeterApplicationKYC,
    MeterApplicationInstallation, MeterPhase,
    MeterApplicationPayment,
)


class MeterApplicationDetailsSerializer(CustomeSerializer):
    customer = serializers.SerializerMethodField()
    class Meta:
        model = MeterApplication
        fields = [
            "pk",
            "uid",
            "customer",
            "customer_name",
            "phone_number",
            "region",
            "region_title",
            "address",
            "request_type",
            "account_number",
            "meter_number",
            "stage",
            "installation_date",
            "get_kyc_information",
            "get_installation_information",
            "get_payment_information",
            "revisions",
            "audits",
            #"kyc_pk",
            #"installation_pk",
            "timestamp",
            "updated",
        ]

    def get_customer(self, obj):
        return f"{obj.customer.pk}"

class MeterApplicationListSerializer(CustomeSerializer):

    class Meta:
        model = MeterApplication
        fields = [
            "pk",
            "uid",
            "customer",
            "customer_name",
            "phone_number",
            "region",
            "region_title",
            "address",
            "request_type",
            "account_number",
            "meter_number",
            "stage",
            "kyc_pk",
            "installation_pk",
            "timestamp",
            "updated",
        ]


class MeterApplicationKYCDetailsSerializer(CustomeSerializer):
    kyc_by = serializers.SerializerMethodField()

    class Meta:
        model = MeterApplicationKYC
        fields = [
            "pk",
            "application",
            "application_uid",
            "app_stage",
            "region",
            "region_title",
            "csp",
            "csp_title",
            "address",
            # "customer",
            "customer_name",
            "account_number",
            "bookcode",
            "meter_number",
            "meter_phase",
            "meter_phase_title",
            "band",
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
            "timestamp",
            "updated",
        ]

    def get_kyc_by(self, obj):
        return f"{obj.kyc_by.pk}"

class MeterApplicationKYCListSerializer(CustomeSerializer):

    class Meta:
        model = MeterApplicationKYC
        fields = [
            "pk",
            "application",
            "application_uid",
            "app_stage",
            "region",
            "region_title",
            "csp",
            "csp_title",
            "address",
            "customer_name",
            "account_number",
            "bookcode",
            "meter_number",
            "band",
            "feeder",
            "feeder_title",
            "transformer",
            "transformer_title",
            "kyc_by",
            "kyc_by_staff",
            "timestamp",
            "updated",
        ]


class MeterPhaseModelSerializer(CustomeSerializer):

    class Meta:
        model = MeterPhase
        fields = [
            "pk",
            "phase",
            "price",
            "active",
            "audits",
            "timestamp",
            "updated",
        ]

###


class MeterApplicationInstallationDetailsSerializer(CustomeSerializer):
    installed_by = serializers.SerializerMethodField()
    class Meta:
        model = MeterApplicationInstallation
        fields = [
            "pk",
            "application",
            "application_uid",
            "meter_number",
            "seal_number",
            "nimsa_seal_number",
            "SGC",
            "FPU",
            "installation_date",
            "installed_by",
            "installed_by_staff",
            "get_vendor",
            "longitude",
            "latitude",
            "altitude",
            "accuracy",
            "audits",
            "timestamp",
            "updated",
        ]

    def get_installed_by(self, obj):
        return f"{obj.installed_by.pk}"


class MeterApplicationInstallationListSerializer(CustomeSerializer):

    class Meta:
        model = MeterApplicationInstallation
        fields = [
            "pk",
            "application",
            "application_uid",
            "meter_number",
            "SGC",
            "FPU",
            "installation_date",
            "installed_by",
            "installed_by_staff",
            "get_vendor",
            "timestamp",
            "updated",
        ]

###


class MeterApplicationPaymentDetailsSerializer(CustomeSerializer):
    approved_by = serializers.SerializerMethodField()

    class Meta:
        model = MeterApplicationPayment
        fields = [
            "pk",
            "application",
            "application_uid",
            "amount",
            "payment_date",
            "mode_of_payment",
            "approved_by",
            "approved_by_staff",
            "get_vendor",
            "audits",
            "timestamp",
            "updated",
        ]

    def get_approved_by(self, obj):
        return f"{obj.approved_by.pk}"


class MeterApplicationPaymentListSerializer(CustomeSerializer):

    class Meta:
        model = MeterApplicationPayment
        fields = [
            "pk",
            "application",
            "application_uid",
            "amount",
            "payment_date",
            "approved_by",
            "approved_by_staff",
            "get_vendor",
            "timestamp",
            "updated",
        ]
