from django.db.utils import IntegrityError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from accounts.models import UserProfile, UserType
from apps.models import Application, UserAppPrivilege, Vendor
from .serializers import (
    ApplicationDetailsSerializer,
    ApplicationListSerializer,
    UserAppPrivilegeDetailsSerializer,
    UserAppPrivilegeListSerializer,
    VendorDetailsSerializer,
    VendorListSerializer,
)

from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()


class ApplicationListAPIView(generics.ListAPIView):
    """Return list of Applications based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of Applications]
    """
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            qs = Application.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class ApplicationSearchAPIView(generics.ListAPIView):
    """Return list of Users based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]
        staff_id: [the staff id of the user]
        username: [the username of the user]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of User Profile]
    """
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            staff_id = self.request.GET.get("staff_id")
            username = self.request.GET.get("username")
            qs = Application.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
            if staff_id:
                qs = qs.filter(staff_id=staff_id)
            if username:
                qs = qs.filter(user__username=username)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class ApplicationDetailsAPIView(generics.RetrieveAPIView):
    """Return Details information of an Application with the given PK

    Args:
        generics ([int]): [pk of the Application]
    """
    serializer_class = ApplicationDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Application.objects.all()



class UserAppPrivilegeUpdateAPIView(generics.UpdateAPIView):
    """Allow update of UserAppPrivilege based on the Query Parameters

    Args:
        pk: [Primary Key of the User App Privilege Relations]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of UserAppPrivilege]
    """
    serializer_class = UserAppPrivilegeDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = UserAppPrivilege.objects.all()
    lookup_field = "pk"


class UserAppPrivilegeListAPIView(generics.ListAPIView):
    """Return list of UserAppPrivilege based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of UserAppPrivilege]
    """
    serializer_class = UserAppPrivilegeListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            qs = UserAppPrivilege.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class UserAppPrivilegeDetailsAPIView(generics.RetrieveAPIView):
    """Return Details information of an UserAppPrivilege with the given PK

    Args:
        pk ([int]): [pk of the UserAppPrivilege]
    """
    serializer_class = UserAppPrivilegeDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserAppPrivilege.objects.all()


class UserAppPrivilegeHistoryAPIView(APIView):
    """Return Details information of the UserAppPrivilege Histories with the given PK

    Args:
        pk ([int]): [pk of the UserAppPrivilege]
    """
    serializer_class = UserAppPrivilegeDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserAppPrivilege.objects.all()

    def get(self, request, pk, format="json"):
        # pk = self.kwargs.get("pk")
        instance = get_object_or_404(UserAppPrivilege, pk=pk)
        # instance_data = UserAppPrivilegeDetailsSerializer(
        #     instance=instance,  context={'request': request})
        dta = {
            "data": instance.get_form_format(),
            "revisions": instance.revisions(),
            "histories": instance.history.all().values()
        }
        status_code = status.HTTP_200_OK

        return Response(data=dta, status=status_code)


class UserAppPrivilegeSearchAPIView(generics.ListAPIView):
    """Return list of UserAppPrivilege based on the Query Parameters

    Args:
        active: [yes for active UserAppPrivilege no for inactive UserAppPrivilege]
        staff_id: [the staff id of the user]
        username: [the username of the user]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of UserAppPrivilege]
    """
    serializer_class = UserAppPrivilegeListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            search_query = self.request.GET.get("search_query")
            qs = UserAppPrivilege.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
            if search_query:
                qs = qs.filter(staff_id=search_query)
            
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class VendorListAPIView(generics.ListAPIView):
    """Return list of Vendors based on the Query Parameters

    Args:
        active: [yes for active users no for inactive users]

    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of Vendors]
    """
    serializer_class = VendorListSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            qs = Vendor.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class VendorSearchAPIView(generics.ListAPIView):
    """Return list of Vendor based on the Search Query
    """
    serializer_class = VendorListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            active = self.request.GET.get("active")
            search_query = self.request.GET.get("search_query")
            qs = Vendor.objects.all()
            if active and active == "yes":
                qs = qs.filter(active=True)
            if active and active == "no":
                qs = qs.filter(active=False)
            if search_query:
                qs = qs.filter(staff_id=search_query)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class VendorDetailsAPIView(generics.RetrieveAPIView):
    """Return Details information of a Vendor with the given PK

    Args:
        generics ([int]): [pk of the Vendor]
    """
    serializer_class = VendorDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Vendor.objects.all()
