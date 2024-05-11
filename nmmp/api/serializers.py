from rest_framework import serializers
from core.api.serializers import CustomeSerializer

from nmmp.models import (
    NMMPKYC,
    NMMPMeter,
    NMMPMeterInstallation,
    NMMPApplicationType,
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
            "application_type",
            "application_type_title",
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

class NMMPKYCListSerializer(CustomeSerializer):

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
            # "customer_name",
            "account_number",
            "bookcode",
            "meter_number",
            "feeder",
            "feeder_title",
            "transformer",
            "transformer_title",
            "kyc_by",
            "kyc_by_staff",
            "stage",
            "timestamp",
            "updated",
        ]

##

##
class NMMPMeterDetailsSerializer(CustomeSerializer):
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = NMMPMeter
        fields = [
            "pk",
            "vendor",
            "vendor_title",
            "meter_number",
            "meter_phase",
            "meter_phase_title",
            "carton_number",
            "SGC",
            "FPU",
            "kyc",
            "assigned",
            "kyc_info",
            "audits",
            "revisions",
            "timestamp",
            "updated",
        ]

    def get_vendor(self, obj):
        return f"{obj.vendor.pk}"

class NMMPMeterListSerializer(CustomeSerializer):

    class Meta:
        model = NMMPMeter
        fields = [
            "pk",
            "vendor",
            "vendor_title",
            "meter_number",
            "meter_phase",
            "meter_phase_title",
            "carton_number",
            "SGC",
            "FPU",
            "kyc",
            "assigned",
            "revisions",
            "timestamp",
            "updated",
        ]

##


class NMMPMeterInstallationDetailsSerializer(CustomeSerializer):
    installed_by = serializers.SerializerMethodField()

    class Meta:
        model = NMMPMeterInstallation
        fields = [
            "pk",
            "kyc",
            "kyc_uid",
            "meter_number",
            "seal_number",
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


class NMMPMeterInstallationListSerializer(CustomeSerializer):

    class Meta:
        model = NMMPMeterInstallation
        fields = [
            "pk",
            "kyc",
            "kyc_uid",
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


##

class NMMPKYCCaptureListSerializer(CustomeSerializer):
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
        model = NMMPKYC
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
        return obj.account_number


    def get_SGC(self, obj):
        return "600296"

    def get_TariffCode(self, obj):
        return obj.band


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
        return f"{obj.last_name}"

    def get_OtherNames(self, obj):
        return f"{obj.first_name} {obj.other_name}"

    def get_CustomerAddress(self, obj):
        return obj.address

    def get_State(self, obj):
        return f"{obj.region.state}"

    def get_CustomerPhone(self, obj):
        return f"{obj.phone_number}"

    def get_E(self, obj):
        return 1

    def get_F(self, obj):
        return 0

    def get_UTID(self, obj):
        return obj.csp.billing_prepaid_id

    def get_TransID(self, obj):
        return obj.transformer.billing_prepaid_id

##


class NMMPARListSerializer(CustomeSerializer):
    """
        NMMP Activity Report
    """
    # application_no = serializers.SerializerMethodField()
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
    FPU = serializers.SerializerMethodField()
    SGC = serializers.SerializerMethodField()
    vendor_name = serializers.SerializerMethodField()
    # amount_paid = serializers.SerializerMethodField()
    # payment_date = serializers.SerializerMethodField()

    class Meta:
        model = NMMPKYC
        fields = [
            "pk",
            # "application_no",
            "uid",
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
            "carton_number",
            "meter_status",
            "installation_date",
            "seal_number",
            "FPU",
            "SGC",
            "vendor_name",
            # "amount_paid",
            # "payment_date",
            "timestamp",
            "updated",
        ]

    # def get_application_no(self, obj):
    #     return f"{obj.uid}"

    def get_first_name(self, obj):
        return f"{obj.first_name}"

    def get_last_name(self, obj):
        return f"{obj.last_name}"

    def get_other_name(self, obj):
        return f"{obj.other_name}"

    def get_address(self, obj):
        return obj.address
        

    def get_phone_no(self, obj):
        return f"{obj.phone_number}"

    def get_meter_no(self, obj):
        return f"{obj.meter_number}"

    def get_account_no(self, obj):
        #return f"{obj.account_number}"
        return obj.account_number

    def get_email(self, obj):
        return f"{obj.email}"

    def get_cin(self, obj):
        return None

    def get_feeder_name(self, obj):
        return obj.feeder.title
       

    def get_csp(self, obj):
        return obj.csp.title
        

    def get_transformer_name(self, obj):
        return obj.transformer.title
        

    def get_service_band(self, obj):
        return obj.band
        
    def get_region(self, obj):
        return obj.region_title()

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
        return obj.premises_type
        

    def get_meter_type(self, obj):
        return obj.meter_phase.phase

    def get_meter_status(self, obj):
        return obj.customer_type

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

    def get_FPU(self, obj):
        return None

    def get_SGC(self, obj):
        return "600296"

    def get_vendor_name(self, obj):
        try:
            return obj.installation.get_vendor
        except Exception as exp:
            return None

    # def get_amount_paid(self, obj):
    #     try:
    #         return obj.paid_amount
    #     except Exception as exp:
    #         return None

    # def get_payment_date(self, obj):
    #     try:
    #         return obj.payment_date
    #     except Exception as exp:
    #         return None


class NMMPApplicationTypeDetailsSerializer(CustomeSerializer):
    class Meta:
        model = NMMPApplicationType
        fields = [
            "pk",
            "title",
            "note",
            "status",
            "nmmpkyc_count",
            "audits",
            "revisions",
            "timestamp",
            "updated",
        ]

class NMMPApplicationTypeListSerializer(CustomeSerializer):
    class Meta:
        model = NMMPApplicationType
        fields = [
            "pk",
            "title",
            "note",
            "status",
            "timestamp",
            "updated",
        ]


