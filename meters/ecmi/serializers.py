#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""

from rest_framework import serializers
from core.api.serializers import CustomeSerializer
from meters.models import MeterApplication

ECMI_CAPTURE_FIELDS = [
    "MeterNumber",
    "AccountNo",
    "SGC",
    "TariffCode",
    "OldSGC",
    "OldTariffCode",
    "A",
    "BUID",
    "B",
    "C",
    "D",
    "Surname",
    "OtherNames",
    "CustomerAddress",
    "State",
    "CustomerPhone",
    "E",
    "F",
    "UTID",
    "TransID",
]


class MeterApplicationCaptureListSerializer(CustomeSerializer):
    MeterNumber = serializers.SerializerMethodField()
    AccountNo = serializers.SerializerMethodField()
    SGC = serializers.SerializerMethodField()
    TariffCode = serializers.SerializerMethodField()
    OldSGC = serializers.SerializerMethodField()
    OldTariffCode = serializers.SerializerMethodField()
    A = serializers.SerializerMethodField()
    BUID = serializers.SerializerMethodField()
    B = serializers.SerializerMethodField()
    C = serializers.SerializerMethodField()
    D = serializers.SerializerMethodField()
    Surname = serializers.SerializerMethodField()
    OtherNames = serializers.SerializerMethodField()
    CustomerAddress = serializers.SerializerMethodField()
    State = serializers.SerializerMethodField()
    CustomerPhone = serializers.SerializerMethodField()
    E = serializers.SerializerMethodField()
    F = serializers.SerializerMethodField()
    UTID = serializers.SerializerMethodField()
    TransID = serializers.SerializerMethodField()
    class Meta:
        model = MeterApplication
        fields = [
            "pk",
            "uid",
            "MeterNumber",
            "AccountNo",
            "SGC",
            "TariffCode",
            "OldSGC",
            "OldTariffCode",
            "A",
            "BUID",
            "B",
            "C",
            "D",
            "Surname",
            "OtherNames",
            "CustomerAddress",
            "State",
            "CustomerPhone",
            "E",
            "F",
            "UTID",
            "TransID",
            "timestamp",
            "updated",
        ]

    def get_MeterNumber(self, obj):
        return f"{obj.meter_number}"

    def get_AccountNo(self, obj):
        #return f"{obj.account_number}"
        try:
            return obj.kyc.account_number
        except Exception as exp:
            return None

    def get_SGC(self, obj):
        return "600296"

    def get_TariffCode(self, obj):
        try:
            return obj.kyc.band
        except Exception as exp:
            print(f"Getting Band From KYC in MeterApplicationCaptureListSerializer: {exp}")
            return None

    def get_OldSGC(self, obj):
        #return "999962"
        try:
            return obj.installation.SGC
        except Exception as exp:
            return None

    def get_OldTariffCode(self, obj):
        return "b1"

    def get_A(self, obj):
        return 0

    def get_BUID(self, obj):
        return f"{obj.region.billing_prepaid_id}"

    def get_B(self, obj):
        return 0
        
    def get_C(self, obj):
        return 0

    def get_D(self, obj):
        return 1
        
    def get_Surname(self, obj):
        return f"{obj.customer.last_name}"

    def get_OtherNames(self, obj):
        return f"{obj.customer.first_name}"

    def get_CustomerAddress(self, obj):
        try:
            return obj.kyc.address
        except Exception as exp:
            return None

    def get_State(self, obj):
        return f"{obj.region.state}"

    def get_CustomerPhone(self, obj):
        return f"{obj.customer.phone_number}"

    def get_E(self, obj):
        return 1

    def get_F(self, obj):
        return 0

    def get_UTID(self, obj):
        try:
            return obj.kyc.csp.billing_prepaid_id
        except Exception as exp:
            return None

    def get_TransID(self, obj):
        try:
            return obj.kyc.transformer.billing_prepaid_id
        except Exception as exp:
            return None


SPAM_FIELDS = [
    'APPLICATION NO', 'First name', 'Last name', 'Other name', 
    ' Address', 'Phone No.',
    'METER NO. (Awaiting Allocation By the System)', 
    'Account No.', 'Email', 'CIN', 'Feeder Name', 'CUSTOMER SERVICE POINT (CSP)', 
    'Transformer Name', 'Service Band (Tariff)',
    'REGION', 'GIS Latitude', 'GIS Longitude', 
    'Building / Premises Type', 'Type of Meter (1Ph/3Ph)', 
    'Meter Status (New / Replacement)', 
    'Date of Installation', ' SEAL NUMBER', 'FPU', 'SGC', 
    'VENDOR NAME', 'AMOUNT PAID', 'DATE OF PAYMENT'
]


class MAPUpfrontPARListSerializer(CustomeSerializer):
    """
        MAP Upfront Payment Activity Report
    """
    application_no = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    other_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    # State = serializers.SerializerMethodField()
    phone_no = serializers.SerializerMethodField()
    meter_no = serializers.SerializerMethodField()
    account_no = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    cin = serializers.SerializerMethodField()
    feeder_name = serializers.SerializerMethodField()
    csp = serializers.SerializerMethodField()
    transformer_name = serializers.SerializerMethodField()
    service_band = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    premises_type = serializers.SerializerMethodField()
    meter_type = serializers.SerializerMethodField()
    meter_status = serializers.SerializerMethodField()
    installation_date = serializers.SerializerMethodField()
    seal_number = serializers.SerializerMethodField()
    nimsa_seal_number = serializers.SerializerMethodField()
    FPU = serializers.SerializerMethodField()
    SGC = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()
    amount_paid = serializers.SerializerMethodField()
    payment_date = serializers.SerializerMethodField()
    

    class Meta:
        model = MeterApplication
        fields = [
            "pk",
            "application_no",
            "stage",
            "first_name",
            "last_name",
            "other_name",
            "address",
            "phone_no",
            "meter_no",
            "account_no",
            "email",
            "cin",
            "feeder_name",
            "csp",
            "transformer_name",
            "service_band",
            "region",
            "latitude",
            "longitude",
            "premises_type",
            "meter_type",
            "meter_status",
            "installation_date",
            "seal_number",
            "nimsa_seal_number",
            "FPU",
            "SGC",
            "vendor_name",
            "amount_paid",
            "payment_date",
            "timestamp",
            "updated",
        ]

    def get_application_no(self, obj):
        return f"{obj.uid}"

    def get_first_name(self, obj):
        return f"{obj.customer.first_name}"

    def get_last_name(self, obj):
        return f"{obj.customer.last_name}"

    def get_other_name(self, obj):
        return None

    def get_address(self, obj):
        try:
            return obj.kyc.address
        except Exception as exp:
            return None

    def get_phone_no(self, obj):
        return f"{obj.customer.phone_number}"

    def get_meter_no(self, obj):
        return f"{obj.meter_number}"

    def get_account_no(self, obj):
        #return f"{obj.account_number}"
        try:
            return obj.kyc.account_number
        except Exception as exp:
            return None

    def get_email(self, obj):
        return f"{obj.customer.get_email}"

    def get_cin(self, obj):
        return None

    def get_feeder_name(self, obj):
        try:
            return obj.kyc.feeder.title
        except Exception as exp:
            return None

    def get_csp(self, obj):
        try:
            return obj.kyc.csp.title
        except Exception as exp:
            return None

    def get_transformer_name(self, obj):
        try:
            return obj.kyc.transformer.title
        except Exception as exp:
            return None

    def get_service_band(self, obj):
        try:
            return obj.kyc.band
        except Exception as exp:
            return None

    def get_region(self, obj):
        try:
            return obj.kyc.region_title()
        except Exception as exp:
            return None

    def get_latitude(self, obj):
        try:
            return obj.installation.latitude
        except Exception as exp:
            return None

    def get_longitude(self, obj):
        try:
            return obj.installation.longitude
        except Exception as exp:
            return None
    
    def get_premises_type(self, obj):
        try:
            return obj.kyc.premises_type
        except Exception as exp:
            return None

    def get_meter_type(self, obj):
        try:
            return obj.kyc.meter_phase.phase
        except Exception as exp:
            return None

    def get_meter_status(self, obj):
        return obj.request_type

    def get_installation_date(self, obj):
        try:
            return obj.installation.installation_date
        except Exception as exp:
            return None

    def get_seal_number(self, obj):
        try:
            return obj.installation.seal_number
        except Exception as exp:
            return None

    def get_nimsa_seal_number(self, obj):
        try:
            return obj.installation.nimsa_seal_number
        except Exception as exp:
            return None

    def get_FPU(self, obj):
        return None

    def get_SGC(self, obj):
        return "600296"

    def get_vendor_name(self, obj):
        try:
            return obj.installation.get_vendor
        except Exception as exp:
            return None

    def get_amount_paid(self, obj):
        try:
            return obj.paid_amount
        except Exception as exp:
            return None

    def get_payment_date(self, obj):
        try:
            return obj.payment_date
        except Exception as exp:
            return None


def boot():
    pass

if __name__ == "__main__":
    boot()
