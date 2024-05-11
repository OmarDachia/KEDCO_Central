from django.db import models
from django.forms import model_to_dict
from accounts.models import UserProfile
from core.abstract_models import CoordinatesModel, TimeStampedModel
from simple_history.models import HistoricalRecords
from core.location.models import Csp, Region
from core.location.nigeria_states import KEDCO_STATE_COVERAGE
from core.utils.units import genserial
from core.utils.core_routings import checkAccountNumber
from gridx.choices import FEEDER_CAPACITY
from gridx.models import Feeder, Station
from md.choices import MD_STAGE_CHOICE
from django.core.validators import FileExtensionValidator


# Create your models here.


class MDMeterApplication(TimeStampedModel):
    """Model for Tracking Maximum Demand customers Meter Application
    """
    uid = models.CharField(max_length=10, default=genserial)
    customer = models.ForeignKey(
        "accounts.CustomerProfile", on_delete=models.PROTECT, related_name="md_meter_applications")
    contractor = models.ForeignKey(
        "accounts.ContractorProfile", on_delete=models.PROTECT, related_name="md_meter_applications")
    company_name = models.CharField(max_length=50)
    company_registration_no = models.CharField(max_length=10)
    company_phone = models.CharField(max_length=50)
    company_email = models.EmailField(unique=True)
    purpose_of_business = models.CharField(max_length=255)
    state = models.CharField(max_length=50, choices=KEDCO_STATE_COVERAGE)
    address = models.CharField(max_length=50)
    account_number = models.CharField(
        max_length=16, blank=True, null=True, validators=[checkAccountNumber]
    )
    meter_number = models.CharField(max_length=15, blank=True, null=True)
    installation_date = models.DateField(blank=True, null=True)
    request_letter = models.FileField(
        blank=True, null=True,upload_to="uploads/md/request_letter", validators=[FileExtensionValidator(['pdf'])])
    # status = models.BooleanField(default=True)
    voltage_level = models.CharField(max_length=5, choices=FEEDER_CAPACITY, blank=True, null=True)
    region = models.ForeignKey(Region, related_name="md_applications", on_delete=models.PROTECT, blank=True, null=True)
    contractor_remark = models.CharField(max_length=255, blank=True, null=True)
    stage = models.CharField(
        max_length=50, choices=MD_STAGE_CHOICE, default="request_initiation")
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "MD Meter Application"
        verbose_name_plural = "MD Meters Applications"
        ordering = ("-updated", "contractor", "company_name",)

    # def save(self, *args, **kwargs):
    #     # self.title = f"{self.title}".capitalize()
    #     super(MDMeterApplication, self).save(*args, **kwargs)

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    @property
    def customer_title(self):
        return f"{self.customer}"

    @property
    def contractor_title(self):
        return f"{self.contractor}"
    
    @property
    def region_title(self):
        return f"{self.region}"

    def __str__(self) -> str:
        return f"{self.uid}"


class MDMeterApplicationInspection(TimeStampedModel, CoordinatesModel):
    """MD Meter Application Inspection

    Args:
        TimeStampedModel (datetime): Timestamp tracting of creation and update
        CoordinatesModel (location coordinates): Latitude, Longitude, Altitude and Accuracy
    """
    application = models.OneToOneField(
        MDMeterApplication, on_delete=models.PROTECT, related_name="inspection")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="md_application_inspection")
    csp = models.ForeignKey(Csp, on_delete=models.PROTECT,related_name="md_application_inspections")
    substation = models.ForeignKey(Station, on_delete=models.PROTECT,related_name="md_application_inspections")
    feeder = models.ForeignKey(Feeder, on_delete=models.PROTECT,related_name="md_application_inspections")
    address = models.CharField(max_length=150)
    trnx_make = models.CharField(max_length=20, help_text="Transformer Make/Type")
    trnx_power_rating = models.CharField(max_length=20, help_text="Transformer Power Rating")
    trnx_current = models.CharField(max_length=20, help_text="Transformer Current HV/LV")
    trnx_impedance = models.CharField(
        max_length=20, help_text="Transformer Impedance")
    trnx_vector_group = models.CharField(max_length=20, help_text="Transformer Vector Group")
    trnx_serial_number = models.CharField(max_length=20, help_text="Transformer Serial Number")
    trnx_manufacture_year= models.CharField(max_length=20, help_text="Transformer Year of Manufacture")
    date_of_test= models.DateField()
    
    # transformer = models.ForeignKey(Transformer, on_delete=models.PROTECT,)
    inspection_by = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, related_name="md_meters_inspections")
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "MD Meter Application Inspection"
        verbose_name_plural = "MD Meter Applications Inspections"
        ordering = ("-updated", )

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def get_form_format(self):
        dta = model_to_dict(self)
        return dta
    
    def application_data(self):
        dta = model_to_dict(self.application)
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

    def application_uid(self):
        return f"{self.application.uid}"

    def app_stage(self):
        return f"{self.application.stage}"

    def meter_phase_title(self):
        return f"{self.meter_phase}"

    def __str__(self) -> str:
        return f"{self.application} - {self.region}"
        
class MDMeterApplicationTrxWindingContinutyTest(TimeStampedModel, CoordinatesModel):
    """
        Inspection: Transformer Continuity Test
    """
    inspection = models.OneToOneField(MDMeterApplicationInspection, on_delete=models.PROTECT, related_name="trx_winding_test")
    r_y = models.IntegerField(help_text="Reading in Mega Ohms")
    y_b = models.IntegerField(help_text="Reading in Mega Ohms")
    b_r = models.IntegerField(help_text="Reading in Mega Ohms")
    r_y_small = models.IntegerField(help_text="Reading in Mega Ohms")
    y_b_small = models.IntegerField(help_text="Reading in Mega Ohms")
    b_r_small = models.IntegerField(help_text="Reading in Mega Ohms")
    r_n = models.IntegerField(help_text="Reading in Mega Ohms")
    y_n = models.IntegerField(help_text="Reading in Mega Ohms")
    b_n = models.IntegerField(help_text="Reading in Mega Ohms")
    
    recorded_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT,)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "MD Meter TRX Winding Test Inspection"
        verbose_name_plural = "MD Meter TRX Winding Test Inspection"
        ordering = ("-updated", )
    
    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()
    
    @property
    def r_y_remark(self):
        return True if self.r_y ==0 else False
        
    @property
    def y_b_remark(self):
        return True if self.y_b ==0 else False
        
    @property
    def b_r_remark(self):
        return True if self.b_r ==0 else False
        
    @property
    def r_y_small_remark(self):
        return True if self.r_y_small ==0 else False
        
    @property
    def y_b_small_remark(self):
        return True if self.y_b_small ==0 else False
        
    @property
    def b_r_small_remark(self):
        return True if self.b_r_small ==0 else False
        
    @property
    def r_n_remark(self):
        return True if self.r_n ==0 else False
        
    @property
    def y_n_remark(self):
        return True if self.y_n ==0 else False
        
    @property
    def b_n_remark(self):
        return True if self.b_n ==0 else False
        
    @property
    def general_remark(self):
        check =  bool(
            self.r_y_remark and
            self.y_b_remark and
            self.b_r_remark and
            self.r_y_small_remark and
            self.y_b_small_remark and
            self.b_r_small_remark and
            self.r_n_remark and
            self.y_n_remark and
            self.b_n_remark
        )
        return "Good" if check else "Faulty"
    
    @property
    def application_uid(self):
        return self.inspection.application.uid
        
        return "Good" if check else "Faulty"
    
    def __str__(self) -> str:
        return f"Trx Winding Continuity Test | {self.inspection}"
    

class MDMeterApplicationTrxWindingInsulationTest(TimeStampedModel, CoordinatesModel):
    """
        Inspection: Transformer Insulation Test
    """
    inspection = models.OneToOneField(
        MDMeterApplicationInspection, on_delete=models.PROTECT, related_name="trx_insulation_test")
    hv_e = models.IntegerField(help_text="Reading in Giga Ohms")
    lv_e = models.IntegerField(help_text="Reading in Giga Ohms")
    hv_lv = models.IntegerField(help_text="Reading in Giga Ohms")

    hv_e_dar = models.IntegerField(help_text="Dielectric Absorption Ratio")
    lv_e_dar = models.IntegerField(help_text="Dielectric Absorption Ratio")
    hv_lv_dar = models.IntegerField(help_text="Dielectric Absorption Ratio")
    

    recorded_by = models.ForeignKey(UserProfile, on_delete=models.PROTECT,)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "MD Meter TRX Winding Test Inspection"
        verbose_name_plural = "MD Meter TRX Winding Test Inspection"
        ordering = ("-updated", )

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    @property
    def hv_e_remark(self):
        return True if self.hv_e >= 500 else False

    @property
    def lv_e_remark(self):
        return True if self.lv_e >= 500 else False

    @property
    def hv_lv_remark(self):
        return True if self.hv_lv >= 500 else False

    @property
    def general_remark(self):
        check = bool(self.hv_e_remark and self.lv_e_remark and self.hv_lv_remark)
        return "Good" if check else "Fails"

    @property
    def application_uid(self):
        return self.inspection.application.uid

    def __str__(self) -> str:
        return f"Trx Winding Insulation Test | {self.inspection}"
