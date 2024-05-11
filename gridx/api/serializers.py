from rest_framework import serializers
from core.api.serializers import CustomeSerializer
from gridx.models import Feeder, Transformer



class FeederDetailsSerializer(CustomeSerializer):

    class Meta:
        model = Feeder
        fields = [
            "pk",
            "title",
            "code",
            "band",
            "capacity",
            "parent_feeder",
            "parent_feeder_title",
            "transformer_count",
            "region",
            "region_title",
            "cavti_id",
            "billing_prepaid_id",
            "billing_postpaid_id",
            "audits",
            "timestamp",
            "updated",
        ]


class FeederListSerializer(CustomeSerializer):

    class Meta:
        model = Feeder
        fields = [
            "pk",
            "title",
            "code",
            "band",
            "capacity",
            "parent_feeder",
            "parent_feeder_title",
            "transformer_count",
            "region",
            "region_title",
            "cavti_id",
            "billing_prepaid_id",
            "billing_postpaid_id",
            "timestamp",
            "updated",
        ]


class TransformerDetailsSerializer(CustomeSerializer):

    class Meta:
        model = Transformer
        fields = [
            "pk",
            "title",
            "code",
            "capacity",
            "ratio",
            "bookcode_1",
            "bookcode_2",
            "bookcode_3",
            "feeder",
            "feeder_title",
            "csp",
            "csp_title",
            "cavti_id",
            "billing_prepaid_id",
            "billing_postpaid_id",
            "audits",
            "timestamp",
            "updated",
        ]


class TransformerListSerializer(CustomeSerializer):

    class Meta:
        model = Transformer
        fields = [
            "pk",
            "title",
            "code",
            "feeder",
            "feeder_title",
            "bookcode_1",
            "csp",
            "csp_title",
            "cavti_id",
            "billing_prepaid_id",
            "billing_postpaid_id",
            "timestamp",
            "updated",
        ]
