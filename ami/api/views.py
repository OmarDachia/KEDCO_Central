from rest_framework import generics, permissions, status, pagination
from rest_framework.response import Response
from django.utils import timezone

from core.api.permissions import HasActiveStaffProfileAPI

from ami.api.serializers import (
    DeviceDetailsSerializer,
    DeviceListSerializer,
    DeviceReadingDetailsSerializer,
    DeviceReadingListSerializer,
)

from ami.models import (
    Device,
    DeviceReading,
)


class DeviceCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of Device
    """

    serializer_class = DeviceDetailsSerializer
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


class DeviceListAPIView(generics.ListAPIView):
    """
       Search and List all Devices based on query parameters
    """

    serializer_class = DeviceListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 200 # Set the number of items per page
    pagination_class.page_size_query_param = 'page_size'  # Allow clients to specify page size in the URL
    # pagination_class.max_page_size = 500  # Optionally, set a maximum page size

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = Device.objects.all().order_by("timestamp")
            search_query = self.request.GET.get("search_query")
            feeder_11 = self.request.GET.get("feeder_11")
            feeder_33 = self.request.GET.get("feeder_33")

            if search_query:
                uid_qs = qs.filter(uid__icontains=search_query)
                meter_number_qs = qs.filter(meter_number__icontains=search_query)
                feeder_11_qs = qs.filter(feeder_11__title__icontains=search_query)
                feeder_33_qs = qs.filter(feeder_33__title__icontains=search_query)
                
                qs = uid_qs | meter_number_qs | feeder_11_qs | feeder_33_qs
            if feeder_11:
                qs = qs.filter(feeder_11=feeder_11)
            if feeder_33:
                qs = qs.filter(feeder_33=feeder_33)
            return qs
        except Exception as exp:
            dta = {
                "detail": "Unable to process your request",
                "error": f"{exp}"
            }
            return Response(dta, status=status.HTTP_400_BAD_REQUEST)


class DeviceDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a Device
    """

    serializer_class = DeviceDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Device.objects.all()
    lookup_field = "uid"


class DeviceUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a Device.
    """

    serializer_class = DeviceDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Device.objects.all()
    lookup_field = "uid"


class DeviceDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of Device
    """

    serializer_class = DeviceDetailsSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Device.objects.all()
    lookup_field = "uid"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"AMI Device (Meter) {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)

#
class DeviceReadingCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of DeviceReading
    """

    serializer_class = DeviceReadingDetailsSerializer
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
        return serializer.save(record_by=self.request.user.profile)


class DeviceReadingListAPIView(generics.ListAPIView):
    """
       Search and List all DeviceReadings based on query parameters
    """

    serializer_class = DeviceReadingListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 200 # Set the number of items per page
    pagination_class.page_size_query_param = 'page_size'  # Allow clients to specify page size in the URL
    # pagination_class.max_page_size = 500  # Optionally, set a maximum page size

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = DeviceReading.objects.all().order_by("timestamp")
            # search_query = self.request.GET.get("search_query")
            # feeder_11 = self.request.GET.get("feeder_11")
            meter = self.request.GET.get("meter")

            # if search_query:
            #     uid_qs = qs.filter(uid__icontains=search_query)
            #     meter_number_qs = qs.filter(meter_number__icontains=search_query)
            #     feeder_11_qs = qs.filter(feeder_11__title__icontains=search_query)
            #     feeder_33_qs = qs.filter(feeder_33__title__icontains=search_query)
                
            #     qs = uid_qs | meter_number_qs | feeder_11_qs | feeder_33_qs
            if meter:
                qs = qs.filter(meter__meter_number=meter)

            return qs
        except Exception as exp:
            dta = {
                "detail": "Unable to process your request",
                "error": f"{exp}"
            }
            return Response(dta, status=status.HTTP_400_BAD_REQUEST)


class DeviceReadingDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a DeviceReading
    """

    serializer_class = DeviceReadingDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = DeviceReading.objects.all()
    lookup_field = "uid"

