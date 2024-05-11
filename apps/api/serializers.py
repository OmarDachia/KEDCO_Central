from rest_framework import serializers
from core.api.serializers import CustomeSerializer
from django.contrib.auth import get_user_model
from apps.models import Application, UserAppPrivilege, Vendor

User = get_user_model()


class ApplicationDetailsSerializer(CustomeSerializer):

    class Meta:
        model = Application
        fields = [
            "pk",
            "title",
            "uid",
            "active",
            "revisions",
            "audits",
            "timestamp",
            "updated",
        ]
class ApplicationListSerializer(CustomeSerializer):

    class Meta:
        model = Application
        fields = [
            "pk",
            "title",
            "uid",
            "active",
            "revisions",
            "timestamp",
            "updated",
        ]


class UserAppPrivilegeDetailsSerializer(CustomeSerializer):

    class Meta:
        model = UserAppPrivilege
        fields = [
            "pk",
            "app",
            "profile",
            "user_type",
            "privileges",
            "access_status",
            "revisions",
            "audits",
            "timestamp",
            "updated",
        ]

class UserAppPrivilegeListSerializer(CustomeSerializer):

    class Meta:
        model = UserAppPrivilege
        fields = [
            "pk",
            "app",
            "profile",
            "user_type",
            "privileges",
            "access_status",
            "revisions",
            "timestamp",
            "updated",
        ]


class VendorDetailsSerializer(CustomeSerializer):

    class Meta:
        model = Vendor
        fields = [
            "pk",
            "uid",
            "title",
            "active",
            "revisions",
            "audits",
            "timestamp",
            "updated",
        ]


class VendorListSerializer(CustomeSerializer):

    class Meta:
        model = Vendor
        fields = [
            "pk",
            "uid",
            "title",
            "active",
            "timestamp",
            "updated",
        ]





