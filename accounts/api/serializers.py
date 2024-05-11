from rest_framework import serializers
from core.api.serializers import CustomeSerializer
from django.contrib.auth import get_user_model
from accounts.models import UserProfile, UserType, CustomerProfile, VendorProfile, ContractorProfile

User = get_user_model()


class UserProfileSerializer(CustomeSerializer):

    class Meta:
        model = UserProfile
        fields = [
            "pk",
            "user",
            "username",
            "first_name",
            "last_name",
            "fullname",
            "is_staff",
            "is_superuser",
            "user_type",
            "active",
            "last_login",
            "get_email",
            "region",
            "region_title",
            "csp",
            "csp_title",
            "groups",
            "user_apps_privileges",
            "timestamp",
            "updated",
        ]


class UserProfileListSerializer(CustomeSerializer):

    class Meta:
        model = UserProfile
        fields = [
            "pk",
            "user",
            "username",
            "fullname",
            "active",
            "get_email",
            "region",
            "region_title",
            "csp",
            "csp_title",
            "timestamp",
            "updated",
        ]


class CustomerProfileDetailsSerializer(CustomeSerializer):

    class Meta:
        model = CustomerProfile
        fields = [
            "pk",
            "user",
            "username",
            "first_name",
            "last_name",
            "fullname",
            "user_type",
            "active",
            "last_login",
            "get_email",
            "phone_number",
            "region",
            "region_title",
            "address",
            "groups",
            "timestamp",
            "updated",
        ]


class CustomerProfileListSerializer(CustomeSerializer):

    class Meta:
        model = CustomerProfile
        fields = [
            "pk",
            "user",
            "username",
            "fullname",
            "phone_number",
            "get_email",
            "active",
            "region",
            "region_title",
            "timestamp",
            "updated",
        ]


###
class VendorProfileDetailsSerializer(CustomeSerializer):

    class Meta:
        model = VendorProfile
        fields = [
            "pk",
            "user",
            "username",
            "fullname",
            "phone_number",
            "get_email",
            "user_type",
            "active",
            "vendor",
            "vendor_title",
            "groups",
            "timestamp",
            "updated",
        ]


class VendorProfileListSerializer(CustomeSerializer):

    class Meta:
        model = VendorProfile
        fields = [
            "pk",
            "user",
            "username",
            "fullname",
            "phone_number",
            "get_email",
            "active",
            "vendor",
            "vendor_title",
            "timestamp",
            "updated",
        ]

###


class ContractorProfileDetailsSerializer(CustomeSerializer):

    class Meta:
        model = ContractorProfile
        fields = [
            "pk",
            "uid",
            "user",
            "username",
            "fullname",
            "phone_number",
            "get_email",
            "user_type",
            "company_name",
            "nemsa_licence",
            "licence_expire_date",
            "last_login",
            "audits",
            "revisions",
            "active",
            "groups",
            "timestamp",
            "updated",
        ]


class ContractorProfileListSerializer(CustomeSerializer):

    class Meta:
        model = ContractorProfile
        fields = [
            "pk",
            "uid",
            "user",
            "username",
            "fullname",
            "phone_number",
            "get_email",
            "active",
            "timestamp",
            "updated",
        ]
