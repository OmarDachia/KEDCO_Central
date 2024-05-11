from django.utils import timezone
from rest_framework import generics, permissions, status, pagination
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from core.api.pagination import CorePagination
from core.api.permissions import HasActiveCustomerProfileAPI, HasActiveStaffProfileAPI, HasActiveVendorProfileAPI, HasActiveContractorProfileAPI
from core.location.models import Region
from md.models import (
    MDMeterApplication,
    MDMeterApplicationInspection,
    MDMeterApplicationTrxWindingContinutyTest,
    MDMeterApplicationTrxWindingInsulationTest,
)
from .serializers import (
    MDMeterApplicationDetailsSerializer,
    MDMeterApplicationListSerializer,
    MDMeterApplicationInspectionDetailsSerializer,
    MDMeterApplicationInspectionListSerializer,
    MDMeterApplicationTrxWindingContinutyTestDetailsSerializer,
    MDMeterApplicationTrxWindingContinutyTestListSerializer,
    MDMeterApplicationTrxWindingInsulationTestDetailsSerializer,
    MDMeterApplicationTrxWindingInsulationTestListSerializer,
)


# Meter Application
class MDMeterApplicationCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of MDMeterApplication
    """

    serializer_class = MDMeterApplicationDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveCustomerProfileAPI,
    ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                    "detail": "Your Details has been captured successfully, Please wait for your contractor to complete the Application.",
                    "data": serializer.data
                }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            data = {
                "detail": "Client Error (Expectation Fail)",
                "error": f"{exp}"
            }
            raise ValidationError(detail=data)

    def perform_create(self, serializer):
        return serializer.save(customer=self.request.user.customer)

class MDMeterApplicationContractorUploadLetter(APIView):
    """
        Allow a Contractor to Upload request letter
    """
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveContractorProfileAPI
    ]

    def post(self, request, format=None):
        md_application_pk = request.POST.get("md_application_pk")
        voltage_level = request.POST.get("voltage_level")
        region_pk = request.POST.get("region_pk")
        contractor_remark = request.POST.get("contractor_remark")
        file_obj = request.FILES.get("request_letter")
        user=request.user
        contractor=user.contractor
        if (
            not  md_application_pk
            or not file_obj
            or not voltage_level
            or not region_pk
        ):
            response = {
                "detail": "Please Provide : md_application_pk and request_letter", 
                "code": 400
            }
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status_code)
        # print(file_obj.content_type)
        if file_obj.content_type != "application/pdf":
            response = {
                "detail": "Only PDF files are allowed!!!",
                "error": f"File received: {file_obj.content_type}"
            }
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status_code)
        if voltage_level not in ["11kva", "33kva"]:
            response = {
                "detail": "Invalid Choice of Voltage level !!!",
                "error": f"voltage level received: {voltage_level}"
            }
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status_code)
        try:
            md_application = get_object_or_404(MDMeterApplication, pk=md_application_pk)
            region = get_object_or_404(
                Region, pk=region_pk)
            if contractor == md_application.contractor:
                md_application.request_letter = file_obj
                md_application.stage = "awaiting_approval"
                md_application.voltage_level = voltage_level
                md_application.region = region
                md_application.contractor_remark = contractor_remark
                md_application.save()
                # TODO: send mail
                response = {"detail": "Request Submitted Successfully, Kindly await a response",}
                status_code = status.HTTP_200_OK
                return Response(response, status=status_code)
            else:
                response = {
                    "detail": "You are not authorize to process this Application",
                    "error": "Contractor mismached!!!",
                }
                status_code = status.HTTP_401_UNAUTHORIZED
                return Response(response, status=status_code)
        except Exception as exp:
            response = {
                "detail": "API Error",
                "error": f"{exp}", 
            }
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status_code)

class MDMeterApplicationListAPIView(generics.ListAPIView):
    """
       List all MDMeterApplications based on query parameters
    """
    serializer_class = MDMeterApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CorePagination
    #CorePagination
    #pagination_class = pagination.PageNumberPagination
    # Optionally, you can customize pagination settings
    #page_size = 500  # Number of items per page
    #page_size_query_param = 'page_size'  # Custom query parameter to override page size
    #max_page_size = 100  # Maximum allowed page size

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MDMeterApplication.objects.all().order_by("timestamp")
            uid = self.request.GET.get("uid")
            region = self.request.GET.get("region")
            stage = self.request.GET.get("stage")
            state = self.request.GET.get("state")
            # stages = self.request.GET.getlist("stages")
            stages = self.request.GET.get("stages")
            if stages and isinstance(stages, str):
                stages = stages.split(",")
            for_customer = self.request.GET.get("for_customer")
            for_contractor = self.request.GET.get("for_contractor")
            user = self.request.user
            if state:
                qs = qs.filter(state=state)
            if uid:
                qs = qs.filter(uid=uid)
            if region:
                qs = qs.filter(region=region)
            if stage:
                qs = qs.filter(stage=stage)
            # if stages and isinstance(stages, list):
            #     print(stages)
            #     qs = qs.filter(stage__in=stages)
            if stages:
                # print(stages)
                qs = qs.filter(stage__in=stages)
            if for_customer and for_customer == "yes":
                qs = qs.filter(customer=user.customer)
            if for_contractor and for_contractor == "yes":
                qs = qs.filter(contractor=user.contractor)
            return qs
        except Exception as exp:
            dta = {
                "detail": f"An Error Occured!! ",
                "errors": f"{exp}"
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)
        
class MDMeterApplicationSearchAPIView(generics.ListAPIView):
    """
       Search and List all MDMeterApplications based on query parameters
    """

    serializer_class = MDMeterApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MDMeterApplication.objects.all().order_by("timestamp")
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
        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs

class MDMeterApplicationDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a MDMeterApplication
    """

    serializer_class = MDMeterApplicationDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MDMeterApplication.objects.all()
    lookup_field = "pk"

class MDMeterApplicationUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a MDMeterApplication.
    """

    serializer_class = MDMeterApplicationDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MDMeterApplication.objects.all()
    lookup_field = "pk"

class MDMeterApplicationDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of MDMeterApplication
    """

    serializer_class = MDMeterApplicationDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MDMeterApplication.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Meter Application {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

## Inspection


class MDMeterApplicationInspectionCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of MDMeterApplicationInspection
    """

    serializer_class = MDMeterApplicationInspectionDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveStaffProfileAPI,
    ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Your Details has been captured successfully",
                "data": serializer.data
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            data = {
                "detail": "Client Error (Expectation Fail)",
                "error": f"{exp}"
            }
            return Response(detail=data)

    def perform_create(self, serializer):
        return serializer.save(inspection_by=self.request.user.profile)


class MDMeterApplicationInspectionListAPIView(generics.ListAPIView):
    """
       List all MDMeterApplicationInspections based on query parameters
    """
    serializer_class = MDMeterApplicationInspectionListSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CorePagination
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 1000


    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MDMeterApplicationInspection.objects.all().order_by("timestamp")
            uid = self.request.GET.get("uid")
            region = self.request.GET.get("region")
            stage = self.request.GET.get("stage")
            state = self.request.GET.get("state")
            # stages = self.request.GET.getlist("stages")
            stages = self.request.GET.get("stages")
            if stages and isinstance(stages, str):
                stages = stages.split(",")
            user = self.request.user
            if state:
                qs = qs.filter(application__state=state)
            if uid:
                qs = qs.filter(application__uid=uid)
            if region:
                qs = qs.filter(application__region=region)
            if stage:
                qs = qs.filter(application__stage=stage)
            # if stages and isinstance(stages, list):
            #     print(stages)
            #     qs = qs.filter(stage__in=stages)
            if stages:
                # print(stages)
                qs = qs.filter(application__stage__in=stages)
            return qs
        except Exception as exp:
            dta = {
                "detail": f"An Error Occured!! ",
                "errors": f"{exp}"
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)


class MDMeterApplicationInspectionSearchAPIView(generics.ListAPIView):
    """
       Search and List all MDMeterApplicationInspections based on query parameters
    """

    serializer_class = MDMeterApplicationInspectionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MDMeterApplicationInspection.objects.all().order_by("timestamp")
            search_query = self.request.GET.get("search_query")
            customer = self.request.GET.get("customer")
            region = self.request.GET.get("region")
            stage = self.request.GET.get("stage")
            if search_query:
                # customer_qs = qs.filter(customer=search_query)
                uid_qs = qs.filter(application__uid=search_query)
                # address_qs = qs.filter(address=search_query)
                # meter_number_qs = qs.filter(meter_number=search_query)
                qs = uid_qs #customer_qs | uid_qs | address_qs | meter_number_qs
            return qs
        except Exception as exp:
            dta = {
                "detail": "Unable to process your request",
                "error": f"{exp}"
            }
            return Response(dta, status=status.HTTP_400_BAD_REQUEST)


class MDMeterApplicationInspectionDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a MDMeterApplicationInspection
    """

    serializer_class = MDMeterApplicationInspectionDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MDMeterApplicationInspection.objects.all()
    lookup_field = "pk"


class MDMeterApplicationInspectionUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a MDMeterApplicationInspection.
    """

    serializer_class = MDMeterApplicationInspectionDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MDMeterApplicationInspection.objects.all()
    lookup_field = "pk"


class MDMeterApplicationInspectionDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of MDMeterApplicationInspection
    """

    serializer_class = MDMeterApplicationInspectionDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MDMeterApplicationInspection.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Meter Application Inspection {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


## Continuity Test

class MDMeterApplicationTrxWindingContinutyTestCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of MDMeterApplicationTrxWindingContinutyTest
    """

    serializer_class = MDMeterApplicationTrxWindingContinutyTestDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveStaffProfileAPI,
    ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Your Details has been captured successfully",
                "data": serializer.data
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            data = {
                "detail": "Client Error (Expectation Fail)",
                "error": f"{exp}"
            }
            return Response(detail=data)

    def perform_create(self, serializer):
        return serializer.save(inspection_by=self.request.user.profile)


class MDMeterApplicationTrxWindingContinutyTestListAPIView(generics.ListAPIView):
    """
       List all MDMeterApplicationTrxWindingContinutyTests based on query parameters
    """
    serializer_class = MDMeterApplicationTrxWindingContinutyTestListSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CorePagination
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 1000

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MDMeterApplicationTrxWindingContinutyTest.objects.all().order_by("timestamp")
            uid = self.request.GET.get("uid")
            region = self.request.GET.get("region")
            stage = self.request.GET.get("stage")
            state = self.request.GET.get("state")
            # stages = self.request.GET.getlist("stages")
            stages = self.request.GET.get("stages")
            if stages and isinstance(stages, str):
                stages = stages.split(",")
            user = self.request.user
            if state:
                qs = qs.filter(inspection__application__state=state)
            if uid:
                qs = qs.filter(inspection__application__uid=uid)
            if region:
                qs = qs.filter(inspection__application__region=region)
            if stage:
                qs = qs.filter(inspection__application__stage=stage)
            # if stages and isinstance(stages, list):
            #     print(stages)
            #     qs = qs.filter(stage__in=stages)
            if stages:
                # print(stages)
                qs = qs.filter(application__stage__in=stages)
            return qs
        except Exception as exp:
            dta = {
                "detail": f"An Error Occured!! ",
                "errors": f"{exp}"
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)


class MDMeterApplicationTrxWindingContinutyTestSearchAPIView(generics.ListAPIView):
    """
       Search and List all MDMeterApplicationTrxWindingContinutyTests based on query parameters
    """

    serializer_class = MDMeterApplicationTrxWindingContinutyTestListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MDMeterApplicationTrxWindingContinutyTest.objects.all().order_by("timestamp")
            search_query = self.request.GET.get("search_query")
            customer = self.request.GET.get("customer")
            region = self.request.GET.get("region")
            stage = self.request.GET.get("stage")
            if search_query:
                # customer_qs = qs.filter(customer=search_query)
                uid_qs = qs.filter(inspection__application__uid=search_query)
                # address_qs = qs.filter(address=search_query)
                # meter_number_qs = qs.filter(meter_number=search_query)
                qs = uid_qs  # customer_qs | uid_qs | address_qs | meter_number_qs
            return qs
        except Exception as exp:
            dta = {
                "detail": "Unable to process your request",
                "error": f"{exp}"
            }
            return Response(dta, status=status.HTTP_400_BAD_REQUEST)


class MDMeterApplicationTrxWindingContinutyTestDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a MDMeterApplicationTrxWindingContinutyTest
    """

    serializer_class = MDMeterApplicationTrxWindingContinutyTestDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MDMeterApplicationTrxWindingContinutyTest.objects.all()
    lookup_field = "pk"


class MDMeterApplicationTrxWindingContinutyTestUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a MDMeterApplicationTrxWindingContinutyTest.
    """

    serializer_class = MDMeterApplicationTrxWindingContinutyTestDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MDMeterApplicationTrxWindingContinutyTest.objects.all()
    lookup_field = "pk"


class MDMeterApplicationTrxWindingContinutyTestDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of MDMeterApplicationTrxWindingContinutyTest
    """

    serializer_class = MDMeterApplicationTrxWindingContinutyTestDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MDMeterApplicationTrxWindingContinutyTest.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {
            "detail": f"Meter Application TrxWindingContinutyTest {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


## Insulation Test

class MDMeterApplicationTrxWindingInsulationTestCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of MDMeterApplicationTrxWindingInsulationTest
    """

    serializer_class = MDMeterApplicationTrxWindingInsulationTestDetailsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasActiveStaffProfileAPI,
    ]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {
                "detail": "Your Details has been captured successfully",
                "data": serializer.data
            }
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            data = {
                "detail": "Client Error (Expectation Fail)",
                "error": f"{exp}"
            }
            return Response(detail=data)

    def perform_create(self, serializer):
        return serializer.save(inspection_by=self.request.user.profile)


class MDMeterApplicationTrxWindingInsulationTestListAPIView(generics.ListAPIView):
    """
       List all MDMeterApplicationTrxWindingInsulationTests based on query parameters
    """
    serializer_class = MDMeterApplicationTrxWindingInsulationTestListSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CorePagination
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 1000

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MDMeterApplicationTrxWindingInsulationTest.objects.all().order_by("timestamp")
            uid = self.request.GET.get("uid")
            region = self.request.GET.get("region")
            stage = self.request.GET.get("stage")
            state = self.request.GET.get("state")
            # stages = self.request.GET.getlist("stages")
            stages = self.request.GET.get("stages")
            if stages and isinstance(stages, str):
                stages = stages.split(",")
            user = self.request.user
            if state:
                qs = qs.filter(inspection__application__state=state)
            if uid:
                qs = qs.filter(inspection__application__uid=uid)
            if region:
                qs = qs.filter(inspection__application__region=region)
            if stage:
                qs = qs.filter(inspection__application__stage=stage)
            # if stages and isinstance(stages, list):
            #     print(stages)
            #     qs = qs.filter(stage__in=stages)
            if stages:
                # print(stages)
                qs = qs.filter(application__stage__in=stages)
            return qs
        except Exception as exp:
            dta = {
                "detail": f"An Error Occured!! ",
                "errors": f"{exp}"
            }
            return Response(data=dta, status=status.HTTP_400_BAD_REQUEST)


class MDMeterApplicationTrxWindingInsulationTestSearchAPIView(generics.ListAPIView):
    """
       Search and List all MDMeterApplicationTrxWindingInsulationTests based on query parameters
    """

    serializer_class = MDMeterApplicationTrxWindingInsulationTestListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = MDMeterApplicationTrxWindingInsulationTest.objects.all().order_by("timestamp")
            search_query = self.request.GET.get("search_query")
            customer = self.request.GET.get("customer")
            region = self.request.GET.get("region")
            stage = self.request.GET.get("stage")
            if search_query:
                # customer_qs = qs.filter(customer=search_query)
                uid_qs = qs.filter(inspection__application__uid=search_query)
                # address_qs = qs.filter(address=search_query)
                # meter_number_qs = qs.filter(meter_number=search_query)
                qs = uid_qs  # customer_qs | uid_qs | address_qs | meter_number_qs
            return qs
        except Exception as exp:
            dta = {
                "detail": "Unable to process your request",
                "error": f"{exp}"
            }
            return Response(dta, status=status.HTTP_400_BAD_REQUEST)


class MDMeterApplicationTrxWindingInsulationTestDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a MDMeterApplicationTrxWindingInsulationTest
    """

    serializer_class = MDMeterApplicationTrxWindingInsulationTestDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MDMeterApplicationTrxWindingInsulationTest.objects.all()
    lookup_field = "pk"


class MDMeterApplicationTrxWindingInsulationTestUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a MDMeterApplicationTrxWindingInsulationTest.
    """

    serializer_class = MDMeterApplicationTrxWindingInsulationTestDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MDMeterApplicationTrxWindingInsulationTest.objects.all()
    lookup_field = "pk"


class MDMeterApplicationTrxWindingInsulationTestDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of MDMeterApplicationTrxWindingInsulationTest
    """

    serializer_class = MDMeterApplicationTrxWindingInsulationTestDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = MDMeterApplicationTrxWindingInsulationTest.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {
            "detail": f"Meter Application TrxWindingContinutyTest {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)
