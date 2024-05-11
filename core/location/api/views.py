from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from core.location.models import State, LGA, Region, Csp
from .serializers import StateModelSerializer, StateModelComboSerializer, LGAModelSerializer, RegionModelSerializer, CspModelSerializer


class StateList(generics.ListAPIView):
    """
       List all States based on query parameters
    """

    serializer_class = StateModelSerializer
    # permission_classes = [permissions.IsAdminUser]

    def get_queryset(self, *args, **kwargs):
        try:
            qs = State.objects.all().order_by("title")
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs


class StateComboList(generics.ListAPIView):
    """
       List all States with their LGAs
    """
    serializer_class = StateModelComboSerializer

    # permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            qs = State.objects.all().order_by("title")
            status_code = status.HTTP_200_OK
        except Exception as exp:
            status_code = status.HTTP_417_EXPECTATION_FAILED
            raise APIException(
                detail=f"An API Exception Occured!!!, Error: {exp}", code=status_code
            )
        return qs

class StateDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a State template
    """

    serializer_class = StateModelComboSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = State.objects.all()
    lookup_field = "pk"


class StateUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a State.
    """

    serializer_class = StateModelSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = State.objects.all()
    lookup_field = "pk"


class StateDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy (delete) a state 
    """

    serializer_class = StateModelSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = State.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"State: {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


# LGA Views
class LGACreateAPIView(generics.CreateAPIView):
    """
       Allows creation of LGA
    """

    serializer_class = LGAModelSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {"detail": "Save Success", "data": serializer.data}
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": [f"Client Error: {exp}"]})


class LGAListAPIView(generics.ListAPIView):
    """
       List all LGAs based on query parameters
    """

    serializer_class = LGAModelSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = LGA.objects.all().order_by("title")
            state_pk = self.request.GET.get("state_pk")
            State_ID = self.request.GET.get("state_id")
            state_code = self.request.GET.get("state_code")
            if state_pk:
                qs = qs.filter(state__pk=state_pk)
            if State_ID:
                qs = qs.filter(state__State_ID=State_ID)
            if state_code:
                qs = qs.filter(state__state_code=state_code)

        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class LGADetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a LGA
    """

    serializer_class = LGAModelSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = LGA.objects.all()
    lookup_field = "pk"


class LGAUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a LGA.
    """

    serializer_class = LGAModelSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = LGA.objects.all()
    lookup_field = "pk"


class LGADeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of LGA
    """

    serializer_class = LGAModelSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = LGA.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"LGA {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


# Region | Csp Views
class RegionCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of Region
    """

    serializer_class = RegionModelSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {"detail": "Save Success", "data": serializer.data}
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": [f"Client Error: {exp}"]})


class RegionListAPIView(generics.ListAPIView):
    """
       List all Regions based on query parameters
    """

    serializer_class = RegionModelSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = Region.objects.all().order_by("title")
            state_pk = self.request.GET.get("state_pk")
            State_ID = self.request.GET.get("state_id")
            state_code = self.request.GET.get("state_code")
            if state_pk:
                qs = qs.filter(state__pk=state_pk)
            if State_ID:
                qs = qs.filter(state__State_ID=State_ID)
            if state_code:
                qs = qs.filter(state__state_code=state_code)

        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class RegionDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a Region
    """

    serializer_class = RegionModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Region.objects.all()
    lookup_field = "pk"


class RegionUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a Region.
    """

    serializer_class = RegionModelSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Region.objects.all()
    lookup_field = "pk"


class RegionDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of Region
    """

    serializer_class = RegionModelSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Region.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Region {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)


class CspCreateAPIView(generics.CreateAPIView):
    """
       Allows creation of Csp
    """

    serializer_class = CspModelSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            dta = {"detail": "Save Success", "data": serializer.data}
            return Response(dta, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as exp:
            raise ValidationError({"detail": [f"Client Error: {exp}"]})


class CspListAPIView(generics.ListAPIView):
    """
       List all Csps based on query parameters
    """

    serializer_class = CspModelSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        today = timezone.localdate()
        try:
            qs = Csp.objects.all().order_by("title")
            state_pk = self.request.GET.get("state_pk")
            State_ID = self.request.GET.get("state_id")
            state_code = self.request.GET.get("state_code")
            region_pk = self.request.GET.get("region_pk")
            if state_pk:
                qs = qs.filter(state__pk=state_pk)
            if State_ID:
                qs = qs.filter(state__State_ID=State_ID)
            if state_code:
                qs = qs.filter(state__state_code=state_code)
            if region_pk:
                qs = qs.filter(region=region_pk)

        except Exception as exp:
            raise ValidationError({"detail": f"Error: {exp}"}) from exp
        return qs


class CspDetailsAPIView(generics.RetrieveAPIView):
    """
       Shows details of a Csp
    """

    serializer_class = CspModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Csp.objects.all()
    lookup_field = "pk"


class CspUpdateAPIView(generics.UpdateAPIView):
    """
       Allows updating of all or parts of a Csp.
    """

    serializer_class = CspModelSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Csp.objects.all()
    lookup_field = "pk"


class CspDeleteAPIView(generics.DestroyAPIView):
    """
       Allows destroy of Csp
    """

    serializer_class = CspModelSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Csp.objects.all()
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        title = f"{instance}"
        self.perform_destroy(instance)
        dta = {"detail": f"Csp {title} Delete Success"}
        return Response(dta, status=status.HTTP_200_OK)
