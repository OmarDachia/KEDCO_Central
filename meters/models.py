from django.db import models
from simple_history.models import HistoricalRecords
from core.abstract_models import CoordinatesModel, TimeStampedModel
from accounts.models import UserProfile, CustomerProfile, VendorProfile
from core.utils.units import genserial
from core.location.models import Csp, Region
from gridx.models import Feeder, Transformer
from meters.choices import CUSTOMER_BAND_CHOICE, MAP_STAGE_CHOICE, METER_APPLICATION_REQUEST_TYPE_CHOICE, PHASE_CHOICE, PREMISES_TYPE_CHOICE
from django.dispatch import receiver
from django.db.models.signals import post_save
from core.utils.core_routings import validateAccountNumber, checkAccountNumber
# Create your models here.





class MeterApplication(TimeStampedModel):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.PROTECT, related_name="meter_applications")
    uid = models.CharField(max_length=10, default=genserial)
    region = models.ForeignKey(
        Region, on_delete=models.PROTECT, related_name="meter_applications"
    )
    address = models.CharField(max_length=150,)
    request_type = models.CharField(
        max_length=20, default="new_request", choices=METER_APPLICATION_REQUEST_TYPE_CHOICE
    )
    account_number = models.CharField(
        max_length=16, blank=True, null=True, validators=[checkAccountNumber]
    )
    meter_number = models.CharField(max_length=15, blank=True, null=True)
    installation_date = models.DateField(blank=True, null=True)
    paid_amount =  models.FloatField(default=0.0)
    payment_date = models.DateField(blank=True, null=True)
    stage = models.CharField(max_length=50, choices=MAP_STAGE_CHOICE)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Meter Application"
        verbose_name_plural = "Meter Applications"
        ordering = ["-updated", ]

    def customer_name(self):
        return f"{self.customer}"

    def phone_number(self):
        return f"{self.customer.phone_number}"

    def region_title(self):
        return f"{self.region}"
    
    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()
        
    def kyc_pk(self):
        try:
            pk = self.kyc.pk
        except Exception as exp:
            #print(exp)
            pk = None
        return pk
            
    def installation_pk(self):
        try:
            pk = self.installation.pk
        except Exception as exp:
            #print(exp)
            pk = None
        return pk

    def get_kyc_information(self):
        try:
            kyc_dta = self.kyc
            dta = kyc_dta.get_form_format()
        except Exception as exp:
            print(exp)
            dta = None
        finally:
            return dta

    def get_installation_information(self):
        try:
            installation_dta = self.installation
            dta = installation_dta.get_form_format()
        except Exception as exp:
            dta = None
        finally:
            return dta
    
    def get_payment_information(self):
        try:
            payment_dta = self.payment
            dta = payment_dta.get_form_format()
        except Exception as exp:
            dta = None
        finally:
            return dta

    def __str__(self) -> str:
        return f"{self.uid} - {self.region}"



class MeterApplicationKYC(TimeStampedModel, CoordinatesModel):
    application = models.OneToOneField(
        MeterApplication, on_delete=models.PROTECT, related_name="kyc")
    region = models.ForeignKey(Region, on_delete=models.PROTECT,)
    csp = models.ForeignKey(Csp, on_delete=models.PROTECT,)
    address = models.CharField(max_length=150)
    account_number = models.CharField(
        max_length=16, blank=True, null=True, validators=[checkAccountNumber]
    )
    bookcode = models.CharField( max_length=10, blank=True, null=True, )
    premises_type = models.CharField(
        max_length=15, choices=PREMISES_TYPE_CHOICE, default="residential"
    )
    customer_type = models.CharField(
        max_length=15, choices=METER_APPLICATION_REQUEST_TYPE_CHOICE, default="new"
    )
    # meter_number = models.CharField(max_length=15,)
    meter_phase = models.ForeignKey("meters.MeterPhase", on_delete=models.PROTECT)
    band = models.CharField(
        max_length=15, choices=CUSTOMER_BAND_CHOICE,  blank=False, null=False)
    feeder = models.ForeignKey(Feeder, on_delete=models.PROTECT,)
    transformer = models.ForeignKey(Transformer, on_delete=models.PROTECT,)
    kyc_by = models.ForeignKey(UserProfile,on_delete=models.PROTECT, related_name="meters_kyc")
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Meter Application KYC"
        verbose_name_plural = "Meter Applications KYC"
        ordering = ["-updated", ]

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def get_form_format(self):
        dta = {
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
        return f"{self.application.customer}"

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

    def meter_number(self):
        return f"{self.application.meter_number}"

    def application_uid(self):
        return f"{self.application.uid}"

    def app_stage(self):
        return f"{self.application.stage}"

    def meter_phase_title(self):
        return f"{self.meter_phase}"

    def __str__(self) -> str:
        return f"{self.application} - {self.region}"


@receiver(post_save, sender=MeterApplicationKYC)
def updateMeterApplicationStatusFromMeterApplicationKYC(sender, instance, created, *args, **kwargs):
    """This signal update MeterApplication status"""
    application = instance.application
    if created:
        application.stage = "awaiting_payment"
        application.save()

class MeterApplicationInstallation(TimeStampedModel, CoordinatesModel):
    application = models.OneToOneField(
        MeterApplication, on_delete=models.PROTECT, related_name="installation")
    meter_number = models.CharField(max_length=15,)
    seal_number = models.CharField(max_length=15, blank=True, null=True)
    nimsa_seal_number = models.CharField(max_length=15, blank=True, null=True)
    SGC = models.PositiveIntegerField(default=999962, help_text="Vendor OLD SGC")
    FPU = models.FloatField(default=0)
    installation_date = models.DateField()
    installed_by = models.ForeignKey(
        VendorProfile, on_delete=models.PROTECT, related_name="meters_installed")
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Meter Application Installation"
        verbose_name_plural = "Meter Applications Installations"
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

    def application_uid(self):
        return f"{self.application.uid}"

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
        return f"{self.application}"


@receiver(post_save, sender=MeterApplicationInstallation)
def updateMeterApplicationStatusInstallation(sender, instance, created, *args, **kwargs):
    """This signal update MeterApplication with Meter Number"""
    application = instance.application
    application.meter_number = instance.meter_number
    application.installation_date = instance.installation_date
    if created:
        if not application.account_number:
            application.stage = "awaiting_account_generation"
        else:
            application.stage = "awaiting_capture"
        # application.save()
    application.save()



class MeterPhase(TimeStampedModel):
    phase = models.CharField(max_length=15, choices=PHASE_CHOICE)
    price = models.FloatField()
    active = models.BooleanField(default=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Meter Phase"
        verbose_name_plural = "Meter Phases"
        ordering = ["-updated", ]


    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()
    
    def __str__(self) -> str:
        return f"{self.phase}"


class MeterApplicationPayment(TimeStampedModel):
    application = models.OneToOneField(
        MeterApplication, on_delete=models.PROTECT, related_name="payment")
    amount = models.FloatField()
    payment_date = models.DateField()
    mode_of_payment = models.CharField(max_length=15, blank=True, null=True)
    approved_by = models.ForeignKey(
        VendorProfile, on_delete=models.PROTECT, related_name="approved_payments"
    )
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Meter Application Payment"
        verbose_name_plural = "Meter Applications Payments"
        ordering = ["-updated", ]

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    @property
    def get_vendor(self):
        return f"{self.approved_by.vendor}"

    @property
    def approved_by_staff(self):
        return f"{self.approved_by}"

    def application_uid(self):
        return f"{self.application.uid}"

    def get_form_format(self):
        dta = {
            "amount": f"{self.amount}",
            "payment_date": f"{self.payment_date}",
            "mode_of_payment": f"{self.mode_of_payment}",
            "approved_by": f"{self.approved_by}",
            "vendor": f"{self.get_vendor}",
        }
        return dta

    def __str__(self) -> str:
        return f"{self.application}"


@receiver(post_save, sender=MeterApplicationPayment)
def updateMeterApplicationStatusFromPayment(sender, instance, created, *args, **kwargs):
    """This signal update MeterApplication with Payment Details"""
    application = instance.application
    application.paid_amount = instance.amount
    application.payment_date = instance.payment_date
    if created:
        application.stage = "awaiting_installation"
        # application.save()
    application.save()
