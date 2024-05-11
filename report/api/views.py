from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from core.api.pagination import CorePagination
from core.api.permissions import HasActiveCustomerProfileAPI, HasActiveStaffProfileAPI, HasActiveVendorProfileAPI
# models
from accounts.models import (
    UserProfile, UserType, CustomerProfile, VendorProfile,
)
from meters.models import (
    MeterApplication, MeterApplicationKYC,
    MeterApplicationInstallation, MeterPhase,
    MeterApplicationPayment,
)
from nmmp.helpers import generateNMMPMeter, generatorNMMPMeter, getValidFPU
from nmmp.models import (
    NMMPKYC,
    NMMPApplicationType,
    NMMPMeter,
    NMMPMeterInstallation,
)

from apps.models import Vendor
from django.conf import settings
from django.core.mail import send_mail
import pandas as pd
from django.contrib.auth import get_user_model


## accounts
class UserStatistics(APIView):
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        User = get_user_model()
        try:
            all_staff = CustomerProfile.objects.all()
            all_customers = CustomerProfile.objects.all()
            all_users = User.objects.all()
            all_vendors = Vendor.objects.all()

            dta = {
                "all_users": all_users.count(),
                "all_staff": all_staff.count(),
                "all_customers": all_customers.count(),
                "all_vendors": all_vendors.count(),
            }
            status_code = status.HTTP_200_OK
            return Response(data=dta, status=status_code)
           
        except Exception as exp:
            dta = {
                "detail": "Client Error",
                "error": f"{exp}"
            }
            status_code = 400         
            return Response(data=dta, status=status_code)


# Meters

class MeterApplicationStatistics(APIView):
    """
        Meter Application Report
    """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            user = request.user
            target_stages = [
                "awaiting_payment", "awaiting_installation",
                "awaiting_account_generation", "awaiting_capture",
                "completed"
            ]
            # qs = NMMPKYC.objects.filter(stage__in=target_stages)
            # date_for = self.request.GET.get("date_for")
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            all_meter_applications = MeterApplication.objects.all()
            all_meter_applications_kyc = MeterApplicationKYC.objects.all()
            all_meter_applications_installation  = MeterApplicationInstallation.objects.all()
            all_meter_applications_payments = MeterApplicationPayment.objects.all()
            if (date_from and not date_to) or (date_to and not date_from):
                status_code = status.HTTP_417_EXPECTATION_FAILED
                raise APIException(
                    detail="date_from and date_to must be used together", code=status_code
                )
            if date_from and date_to:
                all_meter_applications = all_meter_applications.filter(timestamp__date__range=(date_from, date_to))
                all_meter_applications_kyc = all_meter_applications_kyc.filter(timestamp__date__range=(date_from, date_to))
                all_meter_applications_installation = all_meter_applications_installation.filter(timestamp__date__range=(date_from, date_to))
                all_meter_applications_payments = all_meter_applications_payments.filter(timestamp__date__range=(date_from, date_to))
            dta = {
                "message": "All Stats here are for Meter Application (NB: ma=Meter Application)",
                "all_ma": all_meter_applications.count(),
                "ma_awaiting_payment": all_meter_applications.filter(stage="awaiting_payment").count(),
                "ma_awaiting_installation": all_meter_applications.filter(stage="awaiting_installation").count(),
                "ma_awaiting_account_generation": all_meter_applications.filter(stage="awaiting_account_generation").count(),
                "ma_awaiting_capture": all_meter_applications.filter(stage="awaiting_capture").count(),
                "ma_completed": all_meter_applications.filter(stage="completed").count(),
                "kyc-completed": all_meter_applications_kyc.count(),
                "installation_completed": all_meter_applications_installation.count(),
                "payment_completed": all_meter_applications_payments.count(),
            }
            status_code = status.HTTP_200_OK
            return Response(data=dta, status=status_code)
        except Exception as exp:
            dta = {
                "detail": "Client Error",
                "error": f"{exp}"
            }
            status_code = 400
            return Response(data=dta, status=status_code)

# NMMP

class NMMPMeterStatistics(APIView):
    """
        NMMP Meter Application Report
    """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            # qs = NMMPKYC.objects.filter(stage__in=target_stages)
            # date_for = self.request.GET.get("date_for")
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            application_type = self.request.GET.get("application_type")
            all_nmmp_meter_kyc = NMMPKYC.objects.all()
            if application_type:
                all_nmmp_meter_kyc=all_nmmp_meter_kyc.filter(
                    application_type=application_type)
            all_nmmp_meters = NMMPMeter.objects.all()
            all_nmmp_meters_installation = NMMPMeterInstallation.objects.all()
            all_nmmp_application_type = NMMPApplicationType.objects.all()
            if (date_from and not date_to) or (date_to and not date_from):
                status_code = status.HTTP_417_EXPECTATION_FAILED
                raise APIException(
                    detail="date_from and date_to must be used together", code=status_code
                )
            if date_from and date_to:
                all_nmmp_meter_kyc = all_nmmp_meter_kyc.filter(
                    timestamp__date__range=(date_from, date_to))
            dta = {
                "message": "All Stats here are for NMMP Meter Application",
                "all_nmmp": all_nmmp_meter_kyc.count(),
                "nmmp_awaiting_meter": all_nmmp_meter_kyc.filter(stage="awaiting_meter").count(),
                "nmmp_awaiting_capture": all_nmmp_meter_kyc.filter(stage="awaiting_capture").count(),
                "nmmp_awaiting_installation": all_nmmp_meter_kyc.filter(stage="awaiting_installation").count(),
                "nmmp_awaiting_account_generation": all_nmmp_meter_kyc.filter(stage="awaiting_account_generation").count(),
                "nmmp_completed": all_nmmp_meter_kyc.filter(stage="completed").count(),
                # meters
                "all_nmmp_meters": all_nmmp_meters.count(),
                "all_nmmp_meters_installated": all_nmmp_meters_installation.count(),
                "all_nmmp_meters_assigned": all_nmmp_meters.filter(assigned=True).count(),
                "single_phase_nmmp_meters_assigned": all_nmmp_meters.filter(assigned=True, meter_phase__phase="single_phase").count(),
                "two_phase_nmmp_meters_assigned": all_nmmp_meters.filter(assigned=True, meter_phase__phase="two_phase").count(),
                "three_phase_nmmp_meters_assigned": all_nmmp_meters.filter(assigned=True, meter_phase__phase="three_phase").count(),
                "md_nmmp_meters_assigned": all_nmmp_meters.filter(assigned=True, meter_phase__phase="md").count(),
            }
            status_code = status.HTTP_200_OK
            return Response(data=dta, status=status_code)
        except Exception as exp:
            dta = {
                "detail": "Client Error",
                "error": f"{exp}"
            }
            status_code = 400
            return Response(data=dta, status=status_code)


# Vendor

class VendorStatistics(APIView):
    """
        Vendot Report
    """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            # qs = NMMPKYC.objects.filter(stage__in=target_stages)
            # date_for = self.request.GET.get("date_for")
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            all_vendors = Vendor.objects.all()
            all_ma = MeterApplicationInstallation.objects.all()
            all_nmmp_meter_kyc = NMMPKYC.objects.all()
            all_nmmp_meters = NMMPMeter.objects.all()
            all_nmmp_installation = NMMPMeterInstallation.objects.all()
            if (date_from and not date_to) or (date_to and not date_from):
                status_code = status.HTTP_417_EXPECTATION_FAILED
                raise APIException(
                    detail="date_from and date_to must be used together", code=status_code
                )
            if date_from and date_to:
                all_ma = all_ma.filter(
                    timestamp__date__range=(date_from, date_to)
                )
                all_nmmp_meter_kyc = all_nmmp_meter_kyc.filter(
                    timestamp__date__range=(date_from, date_to)
                )
                all_nmmp_meter = all_nmmp_meter.filter(
                    timestamp__date__range=(date_from, date_to)
                )
                all_nmmp_installation = all_nmmp_installation.filter(
                    timestamp__date__range=(date_from, date_to)
                )
            vendors_stats = []
            # print(all_vendors)
            for vendor in all_vendors:
                all_ma_vendor = all_ma.filter(installed_by__vendor=vendor)
                # all_nmmp_meter_kyc_vendor = all_nmmp_meter_kyc.filter(
                #     vendor=vendor)
                all_nmmp_meters_vendor = all_nmmp_meters.filter(vendor=vendor)
                all_nmmp_installation_vendor = all_nmmp_installation.filter(
                    installed_by__vendor=vendor)
                egg = {
                    "vendor_pk": vendor.pk,
                    "vendor_title": f"{vendor}",
                    "staffs": vendor.staffs.all().count(),
                    "ma_installation": all_ma_vendor.count(),
                    # "nmmp_meter_kyc": all_nmmp_meter_kyc.filter(installed_by__vendor=vendor).count(),
                    # "nmmp_meter": all_nmmp_meters.filter(vendor=vendor).count(),
                    # "nmmp_installation": all_nmmp_installation.filter(installed_by__vendor=vendor).count(),
                    #
                    "all_nmmp_meters": all_nmmp_meters_vendor.count(),
                    "all_nmmp_meters_installated": all_nmmp_installation_vendor.count(),
                    "all_nmmp_meters_assigned": all_nmmp_meters_vendor.filter(assigned=True).count(),
                    "all_single_phase_nmmp_meters": all_nmmp_meters_vendor.filter(meter_phase__phase="single_phase").count(),
                    "all_two_phase_nmmp_meters": all_nmmp_meters_vendor.filter(meter_phase__phase="two_phase").count(),
                    "all_three_phase_nmmp_meters": all_nmmp_meters_vendor.filter(meter_phase__phase="three_phase").count(),
                    "all_md_nmmp_meters": all_nmmp_meters_vendor.filter(meter_phase__phase="md").count(),
                    "single_phase_nmmp_meters_assigned": all_nmmp_meters_vendor.filter(assigned=True, meter_phase__phase="single_phase").count(),
                    "two_phase_nmmp_meters_assigned": all_nmmp_meters_vendor.filter(assigned=True, meter_phase__phase="two_phase").count(),
                    "three_phase_nmmp_meters_assigned": all_nmmp_meters_vendor.filter(assigned=True, meter_phase__phase="three_phase").count(),
                    "md_nmmp_meters_assigned": all_nmmp_meters_vendor.filter(assigned=True, meter_phase__phase="md").count(),
                }
                vendors_stats.append(egg)
            dta = {
                "message": "All Stats here are for Vendors",
                "all_ma" : all_ma.count(),
                "ma_installed" : all_ma.count(),
                "all_nmmp_meter_kyc" : all_nmmp_meter_kyc.count(),
                "all_nmmp_meter": all_nmmp_meters.count(),
                "all_nmmp_installation" : all_nmmp_installation.count(),
                "vendors_stats": vendors_stats

            }
            status_code = status.HTTP_200_OK
            return Response(data=dta, status=status_code)
        except Exception as exp:
            dta = {
                "detail": "Client Error",
                "error": f"{exp}"
            }
            status_code = 400
            return Response(data=dta, status=status_code)
