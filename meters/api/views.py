from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from core.api.pagination import CorePagination
from core.api.permissions import HasActiveCustomerProfileAPI, HasActiveStaffProfileAPI, HasActiveVendorProfileAPI
from meters.models import (
    MeterApplication, MeterApplicationKYC,
    MeterApplicationInstallation, MeterPhase,
    MeterApplicationPayment,
)
from .serializers import (
    MeterApplicationDetailsSerializer,
    MeterApplicationListSerializer,
    MeterApplicationKYCDetailsSerializer,
    MeterApplicationKYCListSerializer,
    MeterPhaseModelSerializer,
    MeterApplicationInstallationDetailsSerializer,
    MeterApplicationInstallationListSerializer,
    MeterApplicationPaymentDetailsSerializer,
    MeterApplicationPaymentListSerializer,
)

from meters.ecmi.serializers import (
    MeterApplicationCaptureListSerializer, 
    MAPUpfrontPARListSerializer,
) 

# Meter Application
class MeterApplicationCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of MeterApplication
    """

    serializer_class = MeterApplicationDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveCustomerProfileAPI
    ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                    #"detail": "Meter Application Submitted Successfully",
                    "detail": "Your Details has been captured successfully, our load assesment team will contact for load assessments of your property.",
                   "data": serializer.data
                }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            #raise ValidationError({"detail": [f"Client Error: {exp}"]})
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save(customer=self.request.user.customer)

class MeterApplicationListAPIView(generics.ListAPIView):
    """
       List all MeterApplications based on query parameters
    """
    serializer_class = MeterApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    #pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MeterApplication.objects.all().order_by("-updated")
            customer_pk = self.request.GET.get("customer_pk")
            uid = self.request.GET.get("uid")
            region = self.request.GET.get("region")
            stage = self.request.GET.get("stage")
            for_user = self.request.GET.get("for_user")
            stages = self.request.GET.getlist("stages")
            install_by_user = self.request.GET.get("install_by_user")
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            user = self.request.user
            if customer_pk:
                qs = qs.filter(customer_id=customer_pk)
            if uid:
                qs = qs.filter(uid=uid)
            if region:
                qs = qs.filter(region=region)
            if stage:
                qs = qs.filter(stage=stage)
            if stages and isinstance(stages, list):
                qs = qs.filter(stage__in=stages)
            if for_user and for_user =="yes":
                qs = qs.filter(customer=user.customer)
            if install_by_user and install_by_user =="yes":
                #print("Filtering by Install User")
                user_install_qs = user.vendor.meters_installed.all()
                app_pks_from_install = list(user_install_qs.values_list("application__pk", flat=True))
                #print(app_pks_from_install)
                qs = qs.filter(pk__in=app_pks_from_install)
            #new
            if (date_from and not date_to) or (date_to and not date_from):
                status_code = status.HTTP_417_EXPECTATION_FAILED
                raise APIException(
                    detail="date_from and date_to must be used together", code=status_code
                )
            if date_from and date_to:
                qs = qs.filter(timestamp__date__range=(date_from, date_to))
            #./new
            return qs
        except Exception as exp:
            #raise ValidationError({"detail": f"Error: {exp}"}) from exp
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)
            
class MeterApplicationListAPIViewV2(generics.ListAPIView):
    """
       List all MeterApplications based on query parameters
    """
    serializer_class = MeterApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MeterApplication.objects.all().order_by("-updated")
            customer_pk = self.request.GET.get("customer_pk")
            uid = self.request.GET.get("uid")
            region = self.request.GET.get("region")
            stage = self.request.GET.get("stage")
            for_user = self.request.GET.get("for_user")
            stages = self.request.GET.getlist("stages")
            install_by_user = self.request.GET.get("install_by_user")
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            user = self.request.user
            if customer_pk:
                qs = qs.filter(customer_id=customer_pk)
            if uid:
                qs = qs.filter(uid=uid)
            if region:
                qs = qs.filter(region=region)
            if stage:
                qs = qs.filter(stage=stage)
            if stages and isinstance(stages, list):
                qs = qs.filter(stage__in=stages)
            if for_user and for_user =="yes":
                qs = qs.filter(customer=user.customer)
            if install_by_user and install_by_user =="yes":
                #print("Filtering by Install User")
                user_install_qs = user.vendor.meters_installed.all()
                app_pks_from_install = list(user_install_qs.values_list("application__pk", flat=True))
                #print(app_pks_from_install)
                qs = qs.filter(pk__in=app_pks_from_install)
            #new
            if (date_from and not date_to) or (date_to and not date_from):
                status_code = status.HTTP_417_EXPECTATION_FAILED
                raise APIException(
                    detail="date_from and date_to must be used together", code=status_code
                )
            if date_from and date_to:
                qs = qs.filter(timestamp__date__range=(date_from, date_to))
            #./new
            return qs
        except Exception as exp:
            #raise ValidationError({"detail": f"Error: {exp}"}) from exp
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)


class MeterApplicationSearchAPIView(generics.ListAPIView):
    """
       Search and List all MeterApplications based on query parameters
    """

    serializer_class = MeterApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MeterApplication.objects.all().order_by("timestamp")
            search_query = self.request.GET.get("search_query")
            customer = self.request.GET.get("customer")
            region = self.request.GET.get("region")
            stage = self.request.GET.get("stage")
            if search_query:
                customer_qs = qs.filter(customer=search_query)
                uid_qs = qs.filter(uid=search_query)
                address_qs = qs.filter(address=search_query)
                meter_number_qs = qs.filter(meter_number=search_query)
                qs = customer_qs | uid_qs | address_qs | meter_number_qs
            if customer:
                qs = qs.filter(customer=customer)
            if region:
                qs = qs.filter(region=region)
            if stage:
                qs = qs.filter(stage=stage)
                
            return qs
        except Exception as exp:
            #raise ValidationError({"detail": f"Error: {exp}"}) from exp
            dta = {
                "detail": "Unable to complete request !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)



class MeterApplicationDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a MeterApplication
    """

    serializer_class = MeterApplicationDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MeterApplication.objects.all()
    lookup_field = "pk"


class MeterApplicationUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a MeterApplication.
    """

    serializer_class = MeterApplicationDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MeterApplication.objects.all()
    lookup_field = "pk"


class MeterApplicationDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of MeterApplication
    """

    serializer_class = MeterApplicationDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MeterApplication.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Meter Application {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

##
class MeterApplicationKYCCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of MeterApplicationKYC
    """

    serializer_class = MeterApplicationKYCDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveStaffProfileAPI
    ]

    def create(self, request, *args, **kwargs):
        try:
            print(request.data)
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
            #raise ValidationError({"detail": f"Client Error: {exp}"})
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save(kyc_by=self.request.user.profile)


class MeterApplicationKYCListAPIView(generics.ListAPIView):
    """
       List all MeterApplicationKYCs based on query parameters
    """
    serializer_class = MeterApplicationKYCListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MeterApplicationKYC.objects.all().order_by("timestamp")
            customer_pk = self.request.GET.get("customer_pk")
            region = self.request.GET.get("region")
            csp = self.request.GET.get("csp")
            feeder = self.request.GET.get("feeder")
            transformer = self.request.GET.get("transformer")
            app_stage = self.request.GET.get("app_stage")
            request_type = self.request.GET.get("request_type")
            customer_type = self.request.GET.get("customer_type")
            for_user = self.request.GET.get("for_user")
            user = self.request.user
            if customer_pk:
                qs = qs.filter(customer_id=customer_pk)
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
            if request_type:
                qs = qs.filter(application__request_type=request_type)
            if customer_type:
                qs = qs.filter(customer_type=customer_type)
            if for_user and for_user =="yes":
                qs = qs.filter(customer=user.customer)
            return qs
        except Exception as exp:
            #raise ValidationError({"detail": f"Error: {exp}"}) from exp
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)


class MeterApplicationKYCSearchAPIView(generics.ListAPIView):
    """
       Search and List all MeterApplicationKYCs based on query parameters
    """

    serializer_class = MeterApplicationKYCListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MeterApplicationKYC.objects.all().order_by("timestamp")
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
                address_qs = qs.filter(address__icontains=search_query)
                # meter_number_qs = qs.filter(
                #     meter_number__icontains=search_query)
                qs = uid_qs | address_qs #| meter_number_qs
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
            return qs
        except Exception as exp:
            #raise ValidationError({"detail": f"Error: {exp}"}) from exp
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)



class MeterApplicationKYCDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a MeterApplicationKYC
    """

    serializer_class = MeterApplicationKYCDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MeterApplicationKYC.objects.all()
    lookup_field = "pk"


class MeterApplicationKYCUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a MeterApplicationKYC.
    """

    serializer_class = MeterApplicationKYCDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated, HasActiveStaffProfileAPI]
    queryset = MeterApplicationKYC.objects.all()
    lookup_field = "pk"


class MeterApplicationKYCDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of MeterApplicationKYC
    """

    serializer_class = MeterApplicationKYCDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MeterApplicationKYC.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Meter Application KYC {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

##


class MeterApplicationInstallationCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of MeterApplicationInstallation
    """

    serializer_class = MeterApplicationInstallationDetailsSerializer
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
            #raise ValidationError({"detail": f"Client Error: {exp}"})
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save(installed_by=self.request.user.vendor)


class MeterApplicationInstallationListAPIView(generics.ListAPIView):
    """
       List all MeterApplicationInstallations based on query parameters
    """
    serializer_class = MeterApplicationInstallationListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MeterApplicationInstallation.objects.all().order_by("timestamp")
            customer_pk = self.request.GET.get("customer_pk")
            region = self.request.GET.get("region")
            csp = self.request.GET.get("csp")
            feeder = self.request.GET.get("feeder")
            transformer = self.request.GET.get("transformer")
            app_stage = self.request.GET.get("stage")
            for_user = self.request.GET.get("for_user")
            for_vendor = self.request.GET.get("for_vendor")
            installed_by_user = self.request.GET.get("installed_by_user")
            
            user = self.request.user
            if customer_pk:
                qs = qs.filter(customer_id=customer_pk)
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
            if for_vendor and for_vendor == "yes":
                qs = qs.filter(installed_by__vendor=user.vendor)
            if installed_by_user and installed_by_user == "yes":
                qs = qs.filter(installed_by=user.vendor)
            return qs
        except Exception as exp:
            #raise ValidationError({"detail": f"Error: {exp}"}) from exp
            dta = {
                "detail": "Unqble to complete request !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)



class MeterApplicationInstallationSearchAPIView(generics.ListAPIView):
    """
       Search and List all MeterApplicationInstallations based on query parameters
    """

    serializer_class = MeterApplicationInstallationListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MeterApplicationInstallation.objects.all().order_by("timestamp")
            search_query = self.request.GET.get("search_query")
            customer_pk = self.request.GET.get("customer_pk")
            region = self.request.GET.get("region")
            csp = self.request.GET.get("csp")
            feeder = self.request.GET.get("feeder")
            transformer = self.request.GET.get("transformer")
            app_stage = self.request.GET.get("stage")
            for_user = self.request.GET.get("for_user")
            for_vendor = self.request.GET.get("for_vendor")
            installed_by_user = self.request.GET.get("installed_by_user")
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
                if for_vendor and for_vendor == "yes":
                    qs = qs.filter(installed_by__vendor=user.vendor)
                if installed_by_user and installed_by_user == "yes":
                    qs = qs.filter(installed_by=user.vendor)
                qs = qs.distinct()
            else:
                qs = None
            return qs
        except Exception as exp:
            #raise ValidationError({"detail": f"Error: {exp}"}) from exp
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)



class MeterApplicationInstallationDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a MeterApplicationInstallation
    """

    serializer_class = MeterApplicationInstallationDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MeterApplicationInstallation.objects.all()
    lookup_field = "pk"


class MeterApplicationInstallationUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a MeterApplicationInstallation.
    """

    serializer_class = MeterApplicationInstallationDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated, HasActiveStaffProfileAPI]
    queryset = MeterApplicationInstallation.objects.all()
    lookup_field = "pk"


class MeterApplicationInstallationDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of MeterApplicationInstallation
    """

    serializer_class = MeterApplicationInstallationDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MeterApplicationInstallation.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Meter Application Installation {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

##

class MeterPhaseListAPIView(generics.ListAPIView):
    """
       List all MeterPhase based on query parameters
    """
    serializer_class = MeterPhaseModelSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MeterPhase.objects.all().order_by("timestamp")
            active = self.request.GET.get("active")
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
            return qs
        except Exception as exp:
            #raise ValidationError({"detail": f"Error: {exp}"}) from exp
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)


##


class MeterApplicationPaymentCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of MeterApplicationPayment
    """

    serializer_class = MeterApplicationPaymentDetailsSerializer
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
                "detail": "Payment Information Submitted Successfully",
                "data": serializer.data
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            #raise ValidationError({"detail": f"Client Error: {exp}"})
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        return serializer.save(approved_by=self.request.user.vendor)


class MeterApplicationPaymentListAPIView(generics.ListAPIView):
    """
       List all MeterApplicationPayments based on query parameters
    """
    serializer_class = MeterApplicationPaymentListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MeterApplicationPayment.objects.all().order_by("timestamp")
            customer_pk = self.request.GET.get("customer_pk")
            region = self.request.GET.get("region")
            csp = self.request.GET.get("csp")
            feeder = self.request.GET.get("feeder")
            transformer = self.request.GET.get("transformer")
            app_stage = self.request.GET.get("stage")
            for_user = self.request.GET.get("for_user")
            user = self.request.user
            if customer_pk:
                qs = qs.filter(customer_id=customer_pk)
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
            return qs
        except Exception as exp:
            #raise ValidationError({"detail": f"Error: {exp}"}) from exp
            dta = {
                "detail": "Unable to complete request !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)



class MeterApplicationPaymentSearchAPIView(generics.ListAPIView):
    """
       Search and List all MeterApplicationPayments based on query parameters
    """

    serializer_class = MeterApplicationPaymentListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MeterApplicationPayment.objects.all().order_by("timestamp")
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
            return qs
        except Exception as exp:
            #raise ValidationError({"detail": f"Error: {exp}"}) from exp
            dta = {
                "detail": "Unable to complete request !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)



class MeterApplicationPaymentDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a MeterApplicationPayment
    """

    serializer_class = MeterApplicationPaymentDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MeterApplicationPayment.objects.all()
    lookup_field = "pk"


class MeterApplicationPaymentUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a MeterApplicationPayment.
    """

    serializer_class = MeterApplicationPaymentDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated, HasActiveStaffProfileAPI
    ]
    queryset = MeterApplicationPayment.objects.all()
    lookup_field = "pk"


class MeterApplicationPaymentDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of MeterApplicationPayment
    """

    serializer_class = MeterApplicationPaymentDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MeterApplicationPayment.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Meter Application Payment: {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

##

# Reports
class ECMICaptureListAPIView(generics.ListAPIView):
    serializer_class = MeterApplicationCaptureListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            qs = MeterApplication.objects.filter(stage="awaiting_capture")
            region = self.request.GET.get("region")
            if region:
                qs = qs.filter(region=region)
            status_code = status.HTTP_200_OK
            return qs
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            #raise APIException(
            #    detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            #)
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)



class MAPUpfrontPARListAPIView(generics.ListAPIView):
    """
        MAP Upfront Payment Activity Report
    """
    serializer_class = MAPUpfrontPARListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            target_stage = self.request.GET.get("stage", None)
            target_stages = [
                "awaiting_payment", "awaiting_installation", 
                "awaiting_account_generation", "awaiting_capture", 
                "completed"
            ]
            if target_stage:
                qs = MeterApplication.objects.filter(stage=target_stage)
            else:
                qs = MeterApplication.objects.filter(stage__in=target_stages)
            region = self.request.GET.get("region")
            install_by_user = self.request.GET.get("install_by_user")
            # install_by_user = self.request.GET.get("install_by_user")
            # date_for = self.request.GET.get("date_for")
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            installation_date = self.request.GET.get("installation_date")
            payment_date = self.request.GET.get("payment_date")
            if region:
                qs = qs.filter(region=region)
            if install_by_user and install_by_user =="yes":
                user_install_qs = user.vendor.meters_installed.all()
                app_pks_from_install = user_install_qs.values_list("application__pk", flat=True)
                qs = qs.filter(pk__in=app_pks_from_install)
            # if date_for:
            #     qs = qs.filter(timestamp__date=date_for)
            if (date_from and not date_to) or (date_to and not date_from):
                status_code = status.HTTP_417_EXPECTATION_FAILED
                raise APIException(
                    detail="date_from and date_to must be used together", code=status_code
                )
            if date_from and date_to:
                qs = qs.filter(
                    installation_date__range=(date_from, date_to))
            if installation_date:
                qs = qs.filter(installation_date=installation_date)
            if payment_date:
                qs = qs.filter(payment_date=payment_date)
            
            status_code = status.HTTP_200_OK
            return qs
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            #raise APIException(
            #    detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            #)
            dta = {
                "detail": "Invalid input(s) !!!",
                "error": f"{exp}",
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)



class MAPUpfrontPARListVendorSpecificAPIView(generics.ListAPIView):
    """
        MAP Upfront Payment Activity Report
    """
    serializer_class = MAPUpfrontPARListSerializer
    permission_classes = (permissions.IsAuthenticated, HasActiveVendorProfileAPI)
    pagination_class = CorePagination

    def get_queryset(self, *args, **kwargs):
        try:
            user = self.request.user
            target_stages = [
                "awaiting_payment", "awaiting_installation",
                "awaiting_account_generation", "awaiting_capture",
                "completed"
            ]
            qs = MeterApplication.objects.filter(stage__in=target_stages)
            region = self.request.GET.get("region")
            date_from = self.request.GET.get("date_from")
            date_to = self.request.GET.get("date_to")
            installation_date = self.request.GET.get("installation_date")
            payment_date = self.request.GET.get("payment_date")
            target_vendor = user.vendor.vendor
            # print(target_vendor)
            target_vendor_payments = MeterApplicationPayment.objects.filter(approved_by__vendor=target_vendor)
            target_vendor_payments_application_pks = target_vendor_payments.values_list(
                "application__pk", flat=True)

            qs = qs.filter(pk__in=target_vendor_payments_application_pks)
            if region:
                qs = qs.filter(region=region)
            # if install_by_user and install_by_user == "yes":
            #     user_install_qs = user.vendor.meters_installed.all()
            #     app_pks_from_install = user_install_qs.values_list(
            #         "application__pk", flat=True)
            #     qs = qs.filter(pk__in=app_pks_from_install)
            
            if (date_from and not date_to) or (date_to and not date_from):
                status_code = status.HTTP_417_EXPECTATION_FAILED
                raise APIException(
                    detail="date_from and date_to must be used together", code=status_code
                )
            if date_from and date_to:
                qs = qs.filter(
                    installation_date__range=(date_from, date_to))
            if installation_date:
                qs = qs.filter(installation_date=installation_date)
            if payment_date:
                qs = qs.filter(payment_date=payment_date)

            status_code = status.HTTP_200_OK
            return qs
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            dta = {
                "detail": "An API Exception Occured!!!",
                "error": f"{exp}"
            }
            return Response(
                data=dta, status=status_code
            )
# ./Reports
