from django.db import models
from django.db.models.query_utils import Q
from core.abstract_models import TimeStampedModel
from core.utils.units import LongUniqueId
from accounts.models import UserProfile, UserType
from simple_history.models import HistoricalRecords

from meters.models import MeterApplicationInstallation
# from nmmp.models import NMMPMeter, NMMPMeterInstallation

# Create your models here.

class Application(TimeStampedModel):
    """Model for Tracking Applications and System Developed at SDS Unit of KEDCO ICT

    Args:
        TimeStampedModel ([timestamp, updated]): [Creation, Modification Timestamp]

    Returns:
        [Object]: [Django Model Object Instance of Application]
    """
    title = models.CharField(max_length=50)
    uid = models.UUIDField(default=LongUniqueId, unique=True,)
    active = models.BooleanField(default=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "SDS Application"
        verbose_name_plural = "SDS Applications"
        ordering = ["-updated", "title"]

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".upper()
        super(Application, self).save(*args, **kwargs)

    def audits(self):
        # dta = [audit.values() for audit in self.history.all()]
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def __str__(self) -> str:
        return f"{self.title}"


class UserAppPrivilege(TimeStampedModel):
    """Model for Tracking Applications and User Privileges Relationship

    Args:
        TimeStampedModel ([timestamp, updated]): [Creation, Modification Timestamp]

    Returns:
        [Object]: [Django Model Object Instance of UserAppPrivilege]
    """
    app = models.ForeignKey(Application,limit_choices_to=Q(active=True), on_delete=models.CASCADE, related_name="users")
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="app_privileges")
    user_type = models.ForeignKey(
        UserType, on_delete=models.CASCADE)
    privileges = models.JSONField()
    access_status = models.BooleanField(default=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "User Application Privilege"
        verbose_name_plural = "User Applications Privileges"
        ordering = ["-updated", "app"]
        unique_together = ("app", "profile",)
        
    def get_form_format(self):
        egg = {
            "profile": f"{self.profile}",
            "username": f"{self.profile.user.username}",
            "app_name": f"{self.app.title}",
            "app_uid": f"{self.app.uid}",
            "app_status": self.app.active,
            "status": self.access_status,
            "user_type": f"{self.user_type.title}",
            "user_type_status": self.user_type.status,
            "privileges": self.privileges
        }
        return egg

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def __str__(self) -> str:
        return f"{self.profile} -- {self.app}"


class Vendor(TimeStampedModel):
    """Model for Tracking Vendors
    """
    title = models.CharField(max_length=50)
    uid = models.UUIDField(default=LongUniqueId, unique=True,)
    active = models.BooleanField(default=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"
        ordering = ["-updated", "title"]

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".upper()
        super(Vendor, self).save(*args, **kwargs)

    def audits(self):
        # dta = [audit.values() for audit in self.history.all()]
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()


    def statistics(self):
        dta = {

        }
        return dta

    def __str__(self) -> str:
        return f"{self.title}"
