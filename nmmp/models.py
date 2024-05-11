from operator import mod
from django.conf import settings
from django.db import models
from accounts.models import UserProfile, VendorProfile

from core.abstract_models import CoordinatesModel, TimeStampedModel
from core.choices import STATUS_CHOICE
from core.location.models import Csp, Region
from core.utils.units import genserial
from gridx.models import Feeder, Transformer
from meters.choices import CUSTOMER_BAND_CHOICE, METER_APPLICATION_REQUEST_TYPE_CHOICE, PHASE_CHOICE, PREMISES_TYPE_CHOICE
from meters.models import MeterPhase, checkAccountNumber
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator
from apps.models import Vendor
from nmmp.choices import NMMP_STAGE_CHOICE
from nmmp.utils import nmmp_meters_location
# Create your models here.


class NMMPApplicationType(TimeStampedModel,):
    title = models.CharField(unique=True, max_length=50)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "NMMP Application Type"
        verbose_name_plural = "NMMP Application Types"
        ordering = ("-updated", )

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".upper()
        super(NMMPApplicationType, self).save(*args, **kwargs)

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def nmmpkyc_count(self) -> int:
        return self.nmmpkycs.all().count()

    def __str__(self) -> str:
        return f"{self.title}"


class NMMPKYC(TimeStampedModel, CoordinatesModel):
    uid = models.CharField(max_length=10, default=genserial)
    application_type = models.ForeignKey(NMMPApplicationType, related_name="nmmpkycs", on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    other_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=15, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT,)
    csp = models.ForeignKey(Csp, on_delete=models.PROTECT,)
    address = models.CharField(max_length=150)
    account_number = models.CharField(
        max_length=16, blank=True, null=True, validators=[checkAccountNumber]
    )
    bookcode = models.CharField(max_length=10, blank=True, null=True, )
    premises_type = models.CharField(
        max_length=15, choices=PREMISES_TYPE_CHOICE, 
        # default="residential"
    )
    customer_type = models.CharField(
        max_length=15, choices=METER_APPLICATION_REQUEST_TYPE_CHOICE, 
        # default="new"
    )
    meter_number = models.CharField(max_length=15, blank=True, null=True,)
    meter_phase = models.ForeignKey(
        "meters.MeterPhase", on_delete=models.PROTECT
    )
    band = models.CharField(
        max_length=15, choices=CUSTOMER_BAND_CHOICE,
    )
    feeder = models.ForeignKey(Feeder, on_delete=models.PROTECT,)
    transformer = models.ForeignKey(Transformer, on_delete=models.PROTECT,)
    kyc_by = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name="nmmp_kyc"
    )
    stage = models.CharField(
        max_length=50, choices=NMMP_STAGE_CHOICE, default="awaiting_meter"
    )
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "NMMP KYC"
        verbose_name_plural = "NMMP KYCs"
        ordering = ["-updated", ]

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def application_type_title(self):
        return f"{self.application_type}"
        
    def get_form_format(self):
        dta = {
            "application_type_pk": self.application_type.pk,
            "application_type": f"{self.application_type}",
            "region": f"{self.region}",
            "csp": f"{self.csp}",
            "address": f"{self.address}",
            "account_number": f"{self.account_number}",
            "bookcode": f"{self.bookcode}",
            "meter_phase": f"{self.meter_phase}",
            "band": f"{self.band}",
            "feeder": f"{self.feeder}",
            "transformer": f"{self.transformer}",
            "kyc_by": f"{self.kyc_by}",
        }
        return dta

    def customer_name(self):
        return f"{self.first_name} {self.other_name} {self.last_name}"

    def kyc_by_staff(self):
        return f"{self.kyc_by}"

    def region_title(self):
        return f"{self.region}"

    def csp_title(self):
        return f"{self.csp}"

    def feeder_title(self):
        return f"{self.feeder}"

    def transformer_title(self):
        return f"{self.transformer}"

    def meter_phase_title(self):
        return f"{self.meter_phase}"

    def carton_number(self):
        if self.meter_number:
            try:
                dta = NMMPMeter.objects.get(
                    meter_number=self.meter_number).carton_number
            except NMMPMeter.DoesNotExist as exp:
                dta = False
        else:
            dta = None
        return dta

    def vendor_data(self):
        #TODO: add vendor data from NMMPMeter
        return False

    def __str__(self) -> str:
        return f"{self.uid} - {self.region}"


# @receiver(post_save, sender=NMMPKYC)
# def post_save_NMMPKYC(sender, instance, created, *args, **kwargs):
#     """This signal update NMMPKYC with Meter Number"""
#     application = instance.application
#     if created:
#         available_meters = NMMPMeter.objects.filter(assigned=False)


class NMMPMeterUpload(TimeStampedModel):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.PROTECT, related_name="nmmp_meter_uploads"
    )
    upload_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="nmmp_meters_upload"
    )
    meter_phase = models.ForeignKey(MeterPhase, on_delete=models.PROTECT, )
    meters_file = models.FileField(
        upload_to=nmmp_meters_location,
        validators=[ FileExtensionValidator(["xlsx"]) ]
    )
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "NMMP Meter Upload"
        verbose_name_plural = "NMMP Meter Uploads"
        ordering = ["-updated", ]

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    @property
    def get_vendor(self):
        return f"{self.upload_by.vendor}"

    @property
    def upload_by_staff(self):
        return f"{self.upload_by}"


    def get_form_format(self):
        dta = {
            "upload_by": f"{self.upload_by}",
            "vendor": f"{self.get_vendor}",
            "meters_file": self.meters_file.url,
        }
        return dta

    def __str__(self) -> str:
        return f"{self.kyc}"


class NMMPMeter(TimeStampedModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name="nmmp_meters")
    meter_number = models.CharField(max_length=15, unique=True)
    # phase = models.CharField(max_length=15, choices=PHASE_CHOICE)
    meter_phase = models.ForeignKey(
        "meters.MeterPhase", on_delete=models.PROTECT
    )
    carton_number = models.CharField(max_length=15,)
    SGC = models.PositiveIntegerField()
    FPU = models.FloatField(default=0)
    kyc = models.OneToOneField(NMMPKYC, on_delete=models.SET_NULL, blank=True, null=True, related_name="meter")
    assigned = models.BooleanField(default=False)
    # installed = models.BooleanField(default=False)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "NMMP Meter"
        verbose_name_plural = "NMMP Meters"
        ordering = ["-updated", ]

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def vendor_title(self):
        return f"{self.vendor}"
    
    def meter_phase_title(self):
        return f"{self.meter_phase}"
        
    def kyc_info(self):
        if self.kyc:
            return self.kyc.get_form_format()

    def __str__(self) -> str:
        return f"{self.vendor} - {self.meter_number}"


class NMMPMeterInstallation(TimeStampedModel, CoordinatesModel):
    kyc = models.OneToOneField(
        NMMPKYC, on_delete=models.PROTECT, related_name="installation")
    meter_number = models.CharField(max_length=15,)
    seal_number = models.CharField(max_length=15, blank=True, null=True)
    SGC = models.PositiveIntegerField(
        default=999962, help_text="Vendor OLD SGC")
    FPU = models.FloatField(default=0)
    installation_date = models.DateField()
    installed_by = models.ForeignKey(
        VendorProfile, on_delete=models.PROTECT, related_name="nmmp_meters_installed")
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "NMMP Meter Installation"
        verbose_name_plural = "NMMP Meter Installations"
        ordering = ["-updated", ]

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    @property
    def get_vendor(self):
        return f"{self.installed_by.vendor}"

    @property
    def installed_by_staff(self):
        return f"{self.installed_by}"

    def kyc_uid(self):
        return f"{self.kyc.uid}"

    def get_form_format(self):
        dta = {
            "meter_number": f"{self.meter_number}",
            "seal_number": f"{self.seal_number}",
            "installation_date": f"{self.installation_date}",
            "installed_by": f"{self.installed_by}",
            "vendor": f"{self.get_vendor}",
            "SGC": self.SGC,
            "FPU": self.FPU,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "altitude": self.altitude,
            "accuracy": self.accuracy,
        }
        return dta

    def __str__(self) -> str:
        return f"{self.kyc}"
