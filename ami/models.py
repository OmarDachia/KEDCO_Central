from django.db import models
from accounts.models import UserProfile

from core.abstract_models import TimeStampedModel
from core.utils.units import genserial, getUniqueId
from gridx.models import Feeder, Station, TransmissionStation
from simple_history.models import HistoricalRecords

# Create your models here.
class Device(TimeStampedModel):
    """
        Meter Model
    """
    uid = models.CharField(max_length=10, default=genserial)
    meter_number = models.CharField(max_length=50, unique=True)
    device_pk = models.CharField(max_length=5, unique=True)
    feeder_33 = models.ForeignKey(Feeder,blank=True, null=True, on_delete=models.SET_NULL, related_name="devices_33")
    feeder_11 = models.ForeignKey(Feeder,blank=True, null=True, on_delete=models.SET_NULL, related_name="devices_11")
    voltage_level = models.CharField(max_length=10, blank=True, null=True)
    transmission_station = models.ForeignKey(TransmissionStation, blank=True, null=True, on_delete=models.SET_NULL, related_name="ami_devices")
    injection_substation = models.ForeignKey(Station, blank=True, null=True, on_delete=models.SET_NULL, related_name="ami_devices")
    band = models.CharField(max_length=10, blank=True, null=True)
    commissioned_date = models.CharField(max_length=20, help_text="Date time in Unix Format")

    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "AMI Meter Device"
        verbose_name_plural = "AMI Meter Devices"
        ordering = ("-updated", )

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    @property
    def feeder_33_title(self):
        return f"{self.feeder_33}"
    
    @property
    def feeder_11_title(self):
        return f"{self.feeder_11}"
    
    @property
    def injection_substation_title(self):
        return f"{self.injection_substation}"
    
    @property
    def transmission_station_title(self):
        return f"{self.transmission_station}"


    def __str__(self) -> str:
        return f"{self.meter_number}"
    
class DeviceReading(TimeStampedModel):
    """
        AMI Meter Reading
    """
    uid = models.CharField(max_length=10, default=getUniqueId)
    meter = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="readings")
    reading_timestamp = models.CharField(max_length=20, help_text="Date time in Unix Format")
    VA = models.FloatField(default=0.0)
    VB = models.FloatField(default=0.0)
    VC = models.FloatField(default=0.0)
    IA = models.FloatField(default=0.0)
    IB = models.FloatField(default=0.0)
    IC = models.FloatField(default=0.0)
    PF = models.FloatField(default=0.0)
    MW = models.FloatField(default=0.0)
    MW2 = models.FloatField(default=0.0)
    date = models.DateField()
    time = models.CharField(max_length=4)
    record_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT, related_name="ami_meter_readings")


    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "AMI Meter Reading"
        verbose_name_plural = "AMI Meter Readings"
        ordering = ("-updated", )

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()
    
    @property
    def meter_number(self):
        return f"{self.meter.meter_number}"
    
    def __str__(self) -> str:
        return f"{self.meter} - {self.date} - {self.time}"