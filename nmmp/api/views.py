from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from core.api.pagination import CorePagination
from core.api.permissions import HasActiveCustomerProfileAPI, HasActiveStaffProfileAPI, HasActiveVendorProfileAPI
from meters.models import MeterPhase
from nmmp.helpers import generateNMMPMeter, generatorNMMPMeter, getValidFPU
from nmmp.models import (
    NMMPKYC,
    NMMPMeter,
    NMMPMeterInstallation,
    NMMPMeterUpload,
    NMMPApplicationType,

)
from .serializers import (
    NMMPKYCDetailsSerializer,
    NMMPKYCListSerializer,
    NMMPMeterDetailsSerializer,
    NMMPMeterListSerializer,
    NMMPMeterInstallationDetailsSerializer,
    NMMPMeterInstallationListSerializer,
    NMMPKYCCaptureListSerializer,
    NMMPARListSerializer,
    NMMPApplicationTypeDetailsSerializer,
    NMMPApplicationTypeListSerializer,
)

from apps.models import Vendor
from django.conf import settings
from django.core.mail import send_mail
import pandas as pd


##
class NMMPKYCCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of NMMPKYC
    """

    serializer_class = NMMPKYCDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveStaffProfileAPI
    ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                    "detail": "KYC Information Submitted Successfully",
                   "data": serializer.data
                }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": f"Client Error: {exp}"})

    def perform_create(self, serializer):
        return serializer.save(kyc_by=self.request.user.profile)


class NMMPKYCListAPIView(generics.ListAPIView):
    """
       List all NMMPKYCs based on query parameters
    """
    serializer_class = NMMPKYCListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = NMMPKYC.objects.all().order_by("timestamp")
            application_type = self.request.GET.get("application_type")
            region = self.request.GET.get("region")
            csp = self.request.GET.get("csp")
            feeder = self.request.GET.get("feeder")
            transformer = self.request.GET.get("transformer")
            # app_stage = self.request.GET.get("app_stage")
            # request_type = self.request.GET.get("request_type")
            customer_type = self.request.GET.get("customer_type")
            # for_user = self.request.GET.get("for_user")
            stage = self.request.GET.get("stage")
            date_for = self.request.GET.get("date_for")
            month_for = self.request.GET.get("month_for")
            year_for = self.request.GET.get("year_for")
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            application_type = self.request.GET.get("application_type")
            
            user = self.request.user
            
            if application_type:
                qs = qs.filter(application_type=application_type)
            if region:
                qs = qs.filter(region=region)
            if csp:
                qs = qs.filter(csp=csp)
            if feeder:
                qs = qs.filter(feeder=feeder)
            if transformer:
                qs = qs.filter(transformer=transformer)
            # if app_stage:
            #     qs = qs.filter(application__stage=app_stage)
            if customer_type:
                qs = qs.filter(customer_type=customer_type)
            # if for_user and for_user =="yes":
            #     qs = qs.filter(customer=user.customer)
            if stage:
                qs = qs.filter(stage=stage)
            if date_for:
                qs = qs.filter(timestamp__date=date_for)
            if month_for:
                qs = qs.filter(timestamp__date__month=month_for)
            if year_for:
                qs = qs.filter(timestamp__date__year=year_for)

            if (date_from and not date_to) or (date_to and not date_from):
                status_code = status.HTTP_417_EXPECTATION_FAILED
                raise APIException(
                    detail="date_from and date_to must be used together", code=status_code
                )
            if date_from and date_to:
                qs = qs.filter(timestamp__date__range=(date_from, date_to))
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class NMMPKYCSearchAPIView(generics.ListAPIView):
    """
       Search and List all NMMPKYCs based on query parameters
    """

    serializer_class = NMMPKYCListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = NMMPKYC.objects.all().order_by("timestamp")
            search_query = self.request.GET.get("search_query")
            application_type = self.request.GET.get("application_type")
            region = self.request.GET.get("region")
            csp = self.request.GET.get("csp")
            feeder = self.request.GET.get("feeder")
            transformer = self.request.GET.get("transformer")
            app_stage = self.request.GET.get("stage")
            # for_user = self.request.GET.get("for_user")
            stage = self.request.GET.get("stage")
            date_for = self.request.GET.get("date_for")
            month_for = self.request.GET.get("month_for")
            year_for = self.request.GET.get("year_for")


            user = self.request.user
            
            if search_query:
                # application_qs = qs.filter(
                #     application__title__icontains=search_query)
                first_name_qs = qs.filter(first_name__icontains=search_query)
                address_qs = qs.filter(address__icontains=search_query)
                phone_number_qs = qs.filter(
                    phone_number__icontains=search_query
                )
                qs = first_name_qs | address_qs | phone_number_qs  # | meter_number_qs
                if application_type:
                    qs = qs.filter(application_type=application_type)
                if region:
                    qs = qs.filter(region=region)
                if csp:
                    qs = qs.filter(csp=csp)
                if feeder:
                    qs = qs.filter(feeder=feeder)
                if transformer:
                    qs = qs.filter(transformer=transformer)
                if app_stage:
                    qs = qs.filter(application__stage=app_stage)
                # if for_user and for_user == "yes":
                #     qs = qs.filter(customer=user.customer)
                if stage:
                    qs = qs.filter(stage=stage)
                if stage:
                    qs = qs.filter(stage=stage)
                if date_for:
                    qs = qs.filter(timestamp__date=date_for)
                if month_for:
                    qs = qs.filter(timestamp__date__month=month_for)
                if year_for:
                    qs = qs.filter(timestamp__date__year=year_for)
                qs = qs.distinct()
            else:
                qs = None
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class NMMPKYCDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a NMMPKYC
    """

    serializer_class = NMMPKYCDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = NMMPKYC.objects.all()
    lookup_field = "pk"


class NMMPKYCUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a NMMPKYC.
    """

    serializer_class = NMMPKYCDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated, HasActiveStaffProfileAPI]
    queryset = NMMPKYC.objects.all()
    lookup_field = "pk"


class NMMPKYCDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of NMMPKYC
    """

    serializer_class = NMMPKYCDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = NMMPKYC.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"NMMP KYC {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

##


class AssignMeter(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        nmmp_kyc_pk = request.POST.get("nmmp_kyc_pk")
        vendor_pk = request.POST.get("vendor_pk")
        if (
            not nmmp_kyc_pk
            or not vendor_pk
        ):
            dta = {
                "detail": "Please Provide : nmmp_kyc_pk and vendor_pk", "code": 400
            }
            raise ValidationError(dta)
        try:
            nmmpkyc = get_object_or_404(NMMPKYC, pk=nmmp_kyc_pk)
            vendor = get_object_or_404(Vendor, pk=vendor_pk)
            target_phase = nmmpkyc.meter_phase
            available_meters = NMMPMeter.objects.filter(
                assigned=False,
                # installed=False,
                vendor=vendor_pk,
                meter_phase=target_phase
            ).order_by("carton_number").order_by("meter_number")
            if available_meters.exists():
                target_meter = available_meters.first()
                nmmpkyc.meter_number = target_meter.meter_number
                if nmmpkyc.customer_type == "existing":
                    nmmpkyc.stage = "awaiting_capture"
                else:
                    nmmpkyc.stage = "awaiting_account_generation"
                target_meter.kyc = nmmpkyc
                nmmpkyc.save()
                target_meter.assigned = True
                target_meter.save()
                dta = {
                    "detail": "Meter Successfully Assigned",
                    "data": NMMPKYCDetailsSerializer(instance=nmmpkyc).data
                }
                status_code = status.HTTP_200_OK
                return Response(data=dta, status=status_code)
            else:
                dta = {
                    "detail": f"No Meter Available for Vendor : {vendor}", "code": 400
                }
                # raise ValidationError(dta)
                status_code = status.HTTP_417_EXPECTATION_FAILED
                return Response(data=dta, status=status_code)
        except Exception as exp:
            dta = {"detail": f"Client Error: {exp}"}
            status_code = 400         
            return Response(data=dta, status=status_code)


#

## NMMP Meter
class NMMPMeterUploadAPIView(APIView):
    """
       Allows upload for NMMPMeter by Vendor
    """
    serializer_class = NMMPMeterDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveStaffProfileAPI
        # HasActiveVendorProfileAPI
    ]
    
    expected_columns = [
        # "vendor",
        "meter_number",
        # "meter_phase",
        "carton_number",
        "SGC",
        "FPU",
    ]

    def post(self, request, format=None):
        meter_phase_pk = request.POST.get("meter_phase")
        vendor_pk = request.POST.get("vendor")
        meters_file = request.FILES.get("meters_file")
        upload_by = self.request.user
        if (
            not meter_phase_pk
            or not vendor_pk
            or not meters_file
        ):
            dta = {
                "detail": "Fail to upload Meters, Please Provide Meter `excel file`, `meter_phase` and `vendor`!!"
            }
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise ValidationError(dta,code=status_code)
        vendor = get_object_or_404(Vendor, pk=vendor_pk)
        meter_phase = get_object_or_404(MeterPhase, pk=meter_phase_pk)
        try:
            status_code = status.HTTP_200_OK
            # start timer
            sTime = timezone.now()
            # df = pd.read_csv(meters_file)
            df = pd.read_excel(meters_file, engine="openpyxl")
            data_counts = len(df.index) - 1
            # df = pd.read_excel(meters_file, engine='openpyxl')
            columns = df.columns.tolist()
            result = all(elem in columns for elem in self.expected_columns)
            if result:
                egg = NMMPMeterUpload(
                    upload_by=upload_by,
                    vendor=vendor,
                    meter_phase=meter_phase,
                    meters_file=meters_file,
                )
                egg.save()
                dta = {

                }
                # Saving meters
                # generateNMMPMeter
                # generatorNMMPMeter
                existing_meters = NMMPMeter.objects.all(
                    # vendor=vendor,
                ).values_list("meter_number", flat=True)
                duplicates_meters = [ meter_number for meter_number in df["meter_number"].tolist() if meter_number in existing_meters]
                df = df[~df["meter_number"].isin(existing_meters)]
                meter_numbers = df.meter_number
                duplicates_submission = df[
                    meter_numbers.isin( meter_numbers[meter_numbers.duplicated()] )
                ]
                #
                duplicates_submission = duplicates_submission.meter_number.tolist()
                df = df[~df["meter_number"].isin(duplicates_submission)]
                # purify FPU
                df['FPU'] = df['FPU'].apply(lambda x: getValidFPU(x))
                meters_list = [
                    # generatorNMMPMeter(rows=df.iterrows(), vendor=vendor, meter_phase=meter_phase,) 
                    generateNMMPMeter(row=row, vendor=vendor, meter_phase=meter_phase,) 
                    for i, row in df.iterrows()
                ]
                _ = NMMPMeter.objects.bulk_create(meters_list)
                
                eTime = timezone.now()
                dta["detail"] = f"{data_counts} Meters Successfully Uploaded. Time Elapsed: {eTime-sTime}"
                dta["meters_counts"] = f"{data_counts}"
                dta["meters_uploaded"] = (len(df.index) - 1)
                dta["duplicates"] = len(duplicates_meters)
                dta["duplicates_meters"] = duplicates_meters
                dta["duplicates_submission"] = duplicates_submission
                # from_email = settings.EMAIL_HOST_USER  # "itdevelopkedco@gmail.com"
                # to_emails = [
                #     "ahmadabdulnasir9@gmail.com",
                #     "thezainabmustapha@gmail.com",
                # ]
                # dta["Uploaded_by"] = f"{upload_by}"
                # send_mail(
                #     subject="NMMPMeter UPLOADED",
                #     message=f"Summary: \n{dta}",
                #     from_email=from_email,
                #     recipient_list=to_emails,
                #     fail_silently=True,
                # )
                return Response(dta, status=status_code)
            else:
                dta = {
                    "detail": f"Meters Not Uploaded, Data not in the right format,\
                        expected the following columns: {self.expected_columns}"
                }
                status_code = status.HTTP_403_FORBIDDEN
                return Response(dta, status=status_code)
        except Exception as exp:
            dta = {
                "detail": f"An Error Occur!!!. Error: {exp}"}
            status_code = status.HTTP_417_EXPECTATION_FAILED
            return Response(dta, status=status_code)


class NMMPMeterCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of NMMPMeter
    """

    serializer_class = NMMPMeterDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        # HasActiveStaffProfileAPI
        HasActiveVendorProfileAPI
    ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Meter Information Submitted Successfully",
                "data": serializer.data
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": f"Client Error: {exp}"})

    def perform_create(self, serializer):
        return serializer.save(vendor=self.request.user.vendor.vendor)


class NMMPMeterListAPIView(generics.ListAPIView):
    """
       List all NMMPMeters based on query parameters
    """
    serializer_class = NMMPMeterListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = NMMPMeter.objects.all().order_by("timestamp")
            meter_phase = self.request.GET.get("meter_phase")
            assigned = self.request.GET.get("assigned")
            vendor = self.request.GET.get("vendor")
            user = self.request.user
            if meter_phase:
                qs = qs.filter(meter_phase=meter_phase)
            if assigned and assigned == "yes":
                qs = qs.filter(assigned=True)
            if assigned and assigned == "no":
                qs = qs.filter(assigned=False)
            if vendor:
                qs = qs.filter(vendor=vendor)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class NMMPMeterSearchAPIView(generics.ListAPIView):
    """
       Search and List all NMMPMeters based on query parameters
    """

    serializer_class = NMMPMeterListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = NMMPMeter.objects.all().order_by("timestamp")
            search_query = self.request.GET.get("search_query")
            meter_phase = self.request.GET.get("meter_phase")
            assigned = self.request.GET.get("assigned")
            vendor = self.request.GET.get("vendor")
            user = self.request.user

            if search_query:
                meter_number_qs = qs.filter(meter_number__icontains=search_query)
                carton_number_qs = qs.filter(
                    carton_number__icontains=search_query
                )
                qs = meter_number_qs | carton_number_qs  # | meter_number_qs
                if meter_phase:
                    qs = qs.filter(meter_phase=meter_phase)
                if assigned and assigned == "yes":
                    qs = qs.filter(assigned=True)
                if assigned and assigned == "no":
                    qs = qs.filter(assigned=False)
                if vendor:
                    qs = qs.filter(vendor=vendor)
                qs = qs.distinct()
            else:
                qs = None
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class NMMPMeterDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a NMMPMeter
    """

    serializer_class = NMMPMeterDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = NMMPMeter.objects.all()
    lookup_field = "pk"


class NMMPMeterUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a NMMPMeter.
    """

    serializer_class = NMMPMeterDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated, HasActiveStaffProfileAPI]
    queryset = NMMPMeter.objects.all()
    lookup_field = "pk"


class NMMPMeterDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of NMMPMeter
    """

    serializer_class = NMMPMeterDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = NMMPMeter.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"NMMP Meter {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)
## ./NMMP Meter

## NMMP Installation


class NMMPMeterInstallationCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of NMMPMeterInstallation
    """

    serializer_class = NMMPMeterInstallationDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveVendorProfileAPI
    ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Installation Information Submitted Successfully",
                "data": serializer.data
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": f"Client Error: {exp}"})

    def perform_create(self, serializer):
        return serializer.save(installed_by=self.request.user.vendor)


class NMMPMeterInstallationListAPIView(generics.ListAPIView):
    """
       List all NMMPMeterInstallations based on query parameters
    """
    serializer_class = NMMPMeterInstallationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = NMMPMeterInstallation.objects.all().order_by("timestamp")
            customer_pk = self.request.GET.get("customer_pk")
            region = self.request.GET.get("region")
            csp = self.request.GET.get("csp")
            feeder = self.request.GET.get("feeder")
            transformer = self.request.GET.get("transformer")
            app_stage = self.request.GET.get("stage")
            for_user = self.request.GET.get("for_user")
            user = self.request.user
            for_vendor = self.request.GET.get("for_vendor")
            installed_by_user = self.request.GET.get("installed_by_user")
            if customer_pk:
                qs = qs.filter(customer_id=customer_pk)
            if region:
                qs = qs.filter(kyc__region=region)
            if csp:
                qs = qs.filter(kyc__csp=csp)
            if feeder:
                qs = qs.filter(kyc__feeder=feeder)
            if transformer:
                qs = qs.filter(kyc__transformer=transformer)
            if app_stage:
                qs = qs.filter(application__stage=app_stage)
            if for_user and for_user == "yes":
                qs = qs.filter(customer=user.customer)
            if for_vendor and for_vendor == "yes":
                qs = qs.filter(installed_by__vendor=user.vendor)
            if installed_by_user and installed_by_user == "yes":
                qs = qs.filter(installed_by=user.vendor)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class NMMPMeterInstallationSearchAPIView(generics.ListAPIView):
    """
       Search and List all NMMPMeterInstallations based on query parameters
    """

    serializer_class = NMMPMeterInstallationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = NMMPMeterInstallation.objects.all().order_by("timestamp")
            search_query = self.request.GET.get("search_query")
            customer_pk = self.request.GET.get("customer_pk")
            region = self.request.GET.get("region")
            csp = self.request.GET.get("csp")
            feeder = self.request.GET.get("feeder")
            transformer = self.request.GET.get("transformer")
            app_stage = self.request.GET.get("stage")
            for_user = self.request.GET.get("for_user")
            user = self.request.user

            if search_query:
                # application_qs = qs.filter(
                #     application__title__icontains=search_query)
                uid_qs = qs.filter(application__uid__icontains=search_query)
                address_qs = qs.filter(
                    application__address__icontains=search_query)
                # meter_number_qs = qs.filter(
                #     meter_number__icontains=search_query)
                qs = uid_qs | address_qs  # | meter_number_qs
                if customer_pk:
                    # qs = qs.filter(customer_id=customer_pk)
                    pass
                if region:
                    qs = qs.filter(region=region)
                if csp:
                    qs = qs.filter(csp=csp)
                if feeder:
                    qs = qs.filter(feeder=feeder)
                if transformer:
                    qs = qs.filter(transformer=transformer)
                if app_stage:
                    qs = qs.filter(application__stage=app_stage)
                if for_user and for_user == "yes":
                    qs = qs.filter(customer=user.customer)
                qs = qs.distinct()
            else:
                qs = None
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class NMMPMeterInstallationDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a NMMPMeterInstallation
    """

    serializer_class = NMMPMeterInstallationDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = NMMPMeterInstallation.objects.all()
    lookup_field = "pk"


class NMMPMeterInstallationUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a NMMPMeterInstallation.
    """

    serializer_class = NMMPMeterInstallationDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated, HasActiveStaffProfileAPI]
    queryset = NMMPMeterInstallation.objects.all()
    lookup_field = "pk"


class NMMPMeterInstallationDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of NMMPMeterInstallation
    """

    serializer_class = NMMPMeterInstallationDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = NMMPMeterInstallation.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"NMMP Meter Installation {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


## ./NMMP Installation

## Report

class NMMPECMICaptureListAPIView(generics.ListAPIView):
    serializer_class = NMMPKYCCaptureListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = NMMPKYC.objects.filter(stage="awaiting_capture")
            region = self.request.GET.get("region")
            if region:
                qs = qs.filter(region=region)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class NMMPARListAPIView(generics.ListAPIView):
    """
        MAP Upfront Payment Activity Report
    """
    serializer_class = NMMPARListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            target_stages = [
                "awaiting_meter", "awaiting_installation",
                "awaiting_account_generation", "awaiting_capture",
                "completed"
            ]
            qs = NMMPKYC.objects.filter(stage__in=target_stages)
            region = self.request.GET.get("region")
            install_by_user = self.request.GET.get("install_by_user")
            # date_for = self.request.GET.get("date_for")
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            installation_date = self.request.GET.get("installation_date")
            for_vendor = self.request.GET.get("for_vendor")
            if region:
                qs = qs.filter(region=region)
            if install_by_user and install_by_user == "yes":
                user_install_qs = user.vendor.nmmp_meters_installed.all()
                pks_from_install = list(
                    user_install_qs.values_list("pk", flat=True))
                qs = qs.filter(pk__in=pks_from_install)
            # if date_for:
            #     qs = qs.filter(timestamp__date=date_for)
            if (date_from and not date_to) or (date_to and not date_from):
                status_code = status.HTTP_417_EXPECTATION_FAILED
                raise APIException(
                    detail="date_from and date_to must be used together", code=status_code
                )
            if date_from and date_to:
                qs = qs.filter(
                    timestamp__date__range=(date_from, date_to))
            if installation_date:
                qs = qs.filter(installation_date=installation_date)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class NMMPVendorInstallationListAPIView(generics.ListAPIView):
    """
        Vendors Installation Reports
    """
    serializer_class = NMMPARListSerializer
    permission_classes = [
        permissions.IsAuthenticated, HasActiveVendorProfileAPI]
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            target_stages = [
                "awaiting_payment", "awaiting_installation",
                "awaiting_account_generation", "awaiting_capture",
                "completed"
            ]
            qs = NMMPKYC.objects.filter(
                stage__in=target_stages, meter_number__isnull=False)
            region = self.request.GET.get("region")
            install_by_user = self.request.GET.get("install_by_user")
            # date_for = self.request.GET.get("date_for")
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            installation_date = self.request.GET.get("installation_date")

            vendor_nmmp_meters_qs = user.vendor.vendor.nmmp_meters.all()
            from_vendor_nmmp_meters_numbers = vendor_nmmp_meters_qs.values_list("meter_number", flat=True)
            qs = qs.filter(meter_number__in=from_vendor_nmmp_meters_numbers)
            if region:
                qs = qs.filter(region=region)
            # if date_for:
            #     qs = qs.filter(timestamp__date=date_for)
            if (date_from and not date_to) or (date_to and not date_from):
                status_code = status.HTTP_417_EXPECTATION_FAILED
                raise APIException(
                    detail="date_from and date_to must be used together", code=status_code
                )
            if date_from and date_to:
                qs = qs.filter(
                    timestamp__date__range=(date_from, date_to))
            if installation_date:
                qs = qs.filter(installation_date=installation_date)
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs



## ./Report


## NMMPApplicationType

class NMMPApplicationTypeCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of NMMPApplicationType
    """

    serializer_class = NMMPApplicationTypeDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveStaffProfileAPI
        # HasActiveVendorProfileAPI
    ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "NMMP App. Type Information Submitted Successfully",
                "data": serializer.data
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": f"Client Error: {exp}"})

    def perform_create(self, serializer):
        return serializer.save()


class NMMPApplicationTypeListAPIView(generics.ListAPIView):
    """
       List all NMMPApplicationTypes based on query parameters
    """
    serializer_class = NMMPApplicationTypeListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = NMMPApplicationType.objects.all().order_by("timestamp")
            status_ = self.request.GET.get("status")
            # assigned = self.request.GET.get("assigned")
            # vendor = self.request.GET.get("vendor")
            user = self.request.user
            if status_:
                qs = qs.filter(status=status_)
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class NMMPApplicationTypeSearchAPIView(generics.ListAPIView):
    """
       Search and List all NMMPApplicationTypes based on query parameters
    """

    serializer_class = NMMPApplicationTypeListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = NMMPApplicationType.objects.all().order_by("timestamp")
            search_query = self.request.GET.get("search_query")
            status_ = self.request.GET.get("status")
            user = self.request.user

            if search_query:
                title_qs = qs.filter(
                    title__icontains=search_query)
                note_qs = qs.filter(
                    note__icontains=search_query
                )
                qs = title_qs | note_qs  # | meter_number_qs
                if status_:
                    qs = qs.filter(status=status_)
                qs = qs.distinct()
            else:
                qs = None
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class NMMPApplicationTypeDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a NMMPApplicationType
    """

    serializer_class = NMMPApplicationTypeDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = NMMPApplicationType.objects.all()
    lookup_field = "pk"


class NMMPApplicationTypeUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a NMMPApplicationType.
    """

    serializer_class = NMMPApplicationTypeDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated, HasActiveStaffProfileAPI]
    queryset = NMMPApplicationType.objects.all()
    lookup_field = "pk"


class NMMPApplicationTypeDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of NMMPApplicationType
    """

    serializer_class = NMMPApplicationTypeDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = NMMPApplicationType.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"NMMP Meter {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)
## ./NMMPApplicationType
