from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords

from core.abstract_models import TimeStampedModel
from core.location.models import Region, Csp, State
from .choices import FEEDER_BAND_CHOICE, FEEDER_CAPACITY, FEEDER_TYPES, TRX_CAPACITY
# Create your models here.


class Feeder(TimeStampedModel):
    title = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=50)
    band = models.CharField(max_length=15, choices=FEEDER_BAND_CHOICE)
    capacity = models.CharField(
        max_length=5, choices=FEEDER_CAPACITY, default='11kva')
    parent_feeder = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True,related_name="feeders" )
    cavti_id = models.PositiveIntegerField(blank=True,null=True)
    billing_prepaid_id = models.CharField(max_length=5, blank=True,null=True)
    billing_postpaid_id = models.CharField(max_length=5, blank=True,null=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Feeder"
        verbose_name_plural = "Feeders"
        ordering = ("-updated", )

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".upper()
        super(Feeder, self).save(*args, **kwargs)

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def region_title(self):
        return f"{self.region}"

    def parent_feeder_title(self):
        return f"{self.parent_feeder}"
    
    def transformer_count(self):
        return self.transformers.all().count()

    def __str__(self):
        return str(self.title)


class Transformer(TimeStampedModel):
    title = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=50)
    capacity = models.CharField(max_length=10, blank=True, null=True)
    ratio = models.CharField(max_length=10, blank=True, null=True)
    bookcode_1 = models.CharField(max_length=8)
    bookcode_2 = models.CharField(max_length=8, blank=True, null=True)
    bookcode_3 = models.CharField(max_length=8, blank=True, null=True)
    feeder = models.ForeignKey(Feeder, on_delete=models.PROTECT, related_name="transformers")
    csp = models.ForeignKey(
        Csp, on_delete=models.PROTECT,
        related_name="transformers"
    )
    cavti_id = models.PositiveIntegerField(blank=True, null=True)
    billing_prepaid_id = models.CharField(max_length=5, blank=True, null=True)
    billing_postpaid_id = models.CharField(max_length=5, blank=True, null=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Transformer"
        verbose_name_plural = "Transformers"
        ordering = ("-updated", )

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".upper()
        super(Transformer, self).save(*args, **kwargs)

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def feeder_title(self):
        return f"{self.feeder}"

    def csp_title(self):
        return f"{self.csp}"

    def __str__(self):
        return str(self.title)
        
class TransmissionStation(TimeStampedModel):
    title = models.CharField(max_length=50, unique=True)
    cavti_id = models.PositiveIntegerField(blank=True,null=True)
    state = models.ForeignKey(State, blank=True, null=True, on_delete=models.SET_NULL, related_name="transmission_stations")
    
    history = HistoricalRecords(bases=[TimeStampedModel])
    
    def save(self, *args, **kwargs):
        self.title = f"{self.title}".upper()
        super(TransmissionStation, self).save(*args, **kwargs)

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def __str__(self):
        return f"{self.title}"
              
class Station(TimeStampedModel):
    title = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10)
    capacity = models.CharField(
        max_length=5, choices=FEEDER_CAPACITY, default='11kva')
    transmission = models.ForeignKey(
        TransmissionStation, null=True, blank=True, on_delete=models.SET_NULL, related_name="stations")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True,related_name="regions" )
    cavti_id = models.PositiveIntegerField(blank=True,null=True)
    billing_prepaid_id = models.CharField(max_length=5, blank=True,null=True)
    billing_postpaid_id = models.CharField(max_length=5, blank=True,null=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Injection Substation"
        verbose_name_plural = "Injection Substations"
        ordering = ("-updated", )

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".upper()
        super(Station, self).save(*args, **kwargs)

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def region_title(self):
        return f"{self.region}"

    def transmission_title(self):
        return f"{self.transmission}"
    
   
    def __str__(self):
        return str(self.title)
