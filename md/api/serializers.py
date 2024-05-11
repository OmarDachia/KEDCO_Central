from rest_framework import serializers
from core.api.serializers import CustomeSerializer

from md.models import (
    MDMeterApplication,
    MDMeterApplicationInspection,
    MDMeterApplicationTrxWindingContinutyTest,
    MDMeterApplicationTrxWindingInsulationTest,
)


class MDMeterApplicationDetailsSerializer(CustomeSerializer):
    customer = serializers.SerializerMethodField()
    #contractor = serializers.SerializerMethodField()
    class Meta:
        model = MDMeterApplication
        fields = [
            "pk",
            "uid",
            "customer",
            "customer_title",
            "contractor",
            "contractor_title",
            "company_name",
            "company_registration_no",
            "company_phone",
            "company_email",
            "purpose_of_business",
            "request_letter",
            "state",
            "address",
            "account_number",
            "meter_number",
            "installation_date",
            "voltage_level",
            "region",
            "region_title",
            "contractor_remark",
            "stage",
            # "get_kyc_information",
            # "get_installation_information",
            "revisions",
            "audits",
            #"kyc_pk",
            #"installation_pk",
            "timestamp",
            "updated",
        ]
    read_only_fields = ("request_letter", )

    def get_customer(self, obj):
        return f"{obj.customer.pk}"

    def get_contractor(self, obj):
        return f"{obj.contractor.pk}"

class MDMeterApplicationListSerializer(CustomeSerializer):

    class Meta:
        model = MDMeterApplication
        fields = [
            "pk",
            "uid",
            "contractor",
            "contractor_title",
            "company_name",
            "company_registration_no",
            "company_phone",
            "company_email",
            "state",
            "address",
            "account_number",
            "meter_number",
            "installation_date",
            "stage",
            "voltage_level",
            "region",
            "region_title",
            "contractor_remark",
            "timestamp",
            "updated",
        ]
        
## Inspection
class MDMeterApplicationInspectionDetailsSerializer(CustomeSerializer):
    # customer = serializers.SerializerMethodField()
    #contractor = serializers.SerializerMethodField()
    class Meta:
        model = MDMeterApplicationInspection
        fields = [
            "pk",
            "application",
            "region",
            "csp",
            "substation",
            "feeder",
            "address",
            "trnx_make",
            "trnx_power_rating",
            "trnx_current",
            "trnx_impedance",
            "trnx_vector_group",
            "trnx_serial_number",
            "trnx_manufacture_year",
            "date_of_test",
            "inspection_by",
            "customer_name",
            "region_title",
            "csp_title",
            "feeder_title",
            "application_uid",
            "app_stage",
            "revisions",
            "audits",
            #"kyc_pk",
            #"installation_pk",
            "timestamp",
            "updated",
        ]


class MDMeterApplicationInspectionListSerializer(CustomeSerializer):

    class Meta:
        model = MDMeterApplicationInspection
        fields = [
            "pk",
            "application",
            "region",
            "csp",
            "substation",
            "feeder",
            "address",
            "trnx_make",
            "trnx_power_rating",
            "trnx_current",
            "trnx_impedance",
            "trnx_vector_group",
            "trnx_serial_number",
            "trnx_manufacture_year",
            "date_of_test",
            "timestamp",
            "updated",
        ]

## ./Inspection
## ContinutyTest


class MDMeterApplicationTrxWindingContinutyTestDetailsSerializer(CustomeSerializer):
    # customer = serializers.SerializerMethodField()
    #contractor = serializers.SerializerMethodField()
    class Meta:
        model = MDMeterApplicationTrxWindingContinutyTest
        fields = [
            "pk",
            "inspection",
            "application_uid",
            "r_y",
            "y_b",
            "b_r",
            "r_y_small",
            "y_b_small",
            "b_r_small",
            "r_n",
            "y_n",
            "b_n",
            "recorded_by",
            "r_y_remark",
            "y_b_remark",
            "b_r_remark",
            "r_y_small_remark",
            "y_b_small_remark",
            "b_r_small_remark",
            "r_n_remark",
            "y_n_remark",
            "b_n_remark",
            "general_remark",
            "timestamp",
            "updated",
            "revisions",
            "audits",
        ]


class MDMeterApplicationTrxWindingContinutyTestListSerializer(CustomeSerializer):

    class Meta:
        model = MDMeterApplicationTrxWindingContinutyTest
        fields = [
            "pk",
            "inspection",
            "application_uid",
            "r_y",
            "y_b",
            "b_r",
            "r_y_small",
            "y_b_small",
            "b_r_small",
            "r_n",
            "y_n",
            "b_n",
            "recorded_by",
            "r_y_remark",
            "y_b_remark",
            "b_r_remark",
            "r_y_small_remark",
            "y_b_small_remark",
            "b_r_small_remark",
            "r_n_remark",
            "y_n_remark",
            "b_n_remark",
            "general_remark",
            "timestamp",
            "updated",
            "timestamp",
            "updated",
        ]

## ./ContinutyTest

## InsulationTest
class MDMeterApplicationTrxWindingInsulationTestDetailsSerializer(CustomeSerializer):
    # customer = serializers.SerializerMethodField()
    #contractor = serializers.SerializerMethodField()
    class Meta:
        model = MDMeterApplicationTrxWindingInsulationTest
        fields = [
            "pk",
            "inspection",
            "application_uid",
            "hv_e",
            "lv_e",
            "hv_lv",
            "hv_e_dar",
            "lv_e_dar",
            "hv_lv_dar",
            "hv_e_remark",
            "lv_e_remark",
            "hv_lv_remark",
            "general_remark",
            "recorded_by",
            "timestamp",
            "updated",
            "revisions",
            "audits",
        ]


class MDMeterApplicationTrxWindingInsulationTestListSerializer(CustomeSerializer):

    class Meta:
        model = MDMeterApplicationTrxWindingInsulationTest
        fields = [
            "pk",
            "inspection",
            "application_uid",
            "hv_e",
            "lv_e",
            "hv_lv",
            "hv_e_dar",
            "lv_e_dar",
            "hv_lv_dar",
            "hv_e_remark",
            "lv_e_remark",
            "hv_lv_remark",
            "general_remark",
            "recorded_by",
            "timestamp",
            "updated",
            "timestamp",
            "updated",
        ]

## ./InsulationTest
