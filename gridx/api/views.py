
from rest_framework.exceptions import ValidationError
from gridx.models import Feeder, Transformer
from .serializers import (
    FeederDetailsSerializer,
    FeederListSerializer,
    TransformerDetailsSerializer,
    TransformerListSerializer,
)

from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response



class FeederListAPIView(generics.ListAPIView):
    """Return list of Feeder based on the Query Parameters
    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of Feeder]
    """
    serializer_class = FeederListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            region = self.request.GET.get("region")
            qs = Feeder.objects.all()
            if region:
                qs = qs.filter(region=region)
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class FeederSearchAPIView(generics.ListAPIView):
    """Return list of Feeders based on the Search Query
    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of Feeders]
    """
    serializer_class = FeederListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            search_query = self.request.GET.get("search_query")
            region = self.request.GET.get("region")
            qs = Feeder.objects.all()
            if search_query :
                title_qs = qs.filter(title__icontains=search_query)
                code_qs = qs.filter(code__icontains=search_query)
                parent_feeder_qs = qs.filter(
                    parent_feeder__title__icontains=search_query)
                combo_qs = title_qs | code_qs | parent_feeder_qs
                qs = combo_qs.distinct()
                if region:
                    qs = qs.filter(region=region)
            else:
                qs = None
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class FeederDetailsAPIView(generics.RetrieveAPIView):
    """Return Details information of an Feeder with the given PK

    Args:
        generics ([int]): [pk of the Feeder]
    """
    serializer_class = FeederDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Feeder.objects.all()
    lookup_field = "pk"


class TransformerListAPIView(generics.ListAPIView):
    """Return list of Transformer based on the Query Parameters
    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of Transformer]
    """
    serializer_class = TransformerListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            feeder = self.request.GET.get("feeder")
            csp = self.request.GET.get("csp")
            qs = Transformer.objects.all()
            if feeder:
                qs = qs.filter(feeder=feeder)
            if csp:
                qs = qs.filter(csp=csp)
           
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class TransformerSearchAPIView(generics.ListAPIView):
    """Return list of Transformers based on the Search Query
    Raises:
        ValidationError: [Raise Validation Error if any error occur during processing query params]

    Returns:
        [List]: [List of Transformers]
    """
    serializer_class = TransformerListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        try:
            feeder = self.request.GET.get("feeder")
            search_query = self.request.GET.get("search_query")
            qs = Transformer.objects.all()
            if search_query:
                title_qs = qs.filter(title__icontains=search_query)
                code_qs = qs.filter(code__icontains=search_query)
                feeder_qs = qs.filter(feeder__title__icontains=search_query)
                combo_qs = title_qs | code_qs | feeder_qs
                qs = combo_qs.distinct()
                if feeder:
                    qs = qs.filter(feeder=feeder)
            else:
                qs = None
            
        except Exception as error:
            raise ValidationError({"detail": f"Error: {error}"}) from error
        return qs


class TransformerDetailsAPIView(generics.RetrieveAPIView):
    """Return Details information of an Transformer with the given PK

    Args:
        generics ([int]): [pk of the Transformer]
    """
    serializer_class = TransformerDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Transformer.objects.all()
    lookup_field = "pk"
