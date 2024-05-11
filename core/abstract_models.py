from django.db import models
# from accounts.models import Marchant, Store

class TimeStampedModel(models.Model):
    """
    Abstract base model with fields for tracking object creation and last
    update dates.
    """

    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class KEDCORegionCspModel(models.Model):
    """
    Abstract base model with fields for tracking object Feeder, Region and CSP
    """

    region = models.ForeignKey("core.location.Region", on_delete=models.CASCADE,)
    csp = models.ForeignKey("core.location.Csp", on_delete=models.CASCADE,)
    
    class Meta:
        abstract = True


class CoordinatesModel(models.Model):
    """
    Abstract base model with fields for tracking coordinates
    """

    longitude = models.FloatField()
    latitude = models.FloatField()
    altitude = models.FloatField()
    accuracy = models.FloatField()

    class Meta:
        abstract = True
