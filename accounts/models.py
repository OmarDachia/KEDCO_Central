import re
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.db import models
from accounts.choices import USER_TYPE_CHOICE
# from apps.models import Vendor

from core.abstract_models import TimeStampedModel
from django.conf import settings
# from core.utils.core_routings import is_valid_nimsa

from core.utils.units import LongUniqueId, genserial
from django.core.validators import (
    MinLengthValidator,
)
from django.core.exceptions import ValidationError


from simple_history.models import HistoricalRecords

from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

from django.core.mail import send_mail
from django.utils import timezone #, timedelta


# Create your models here.
class UserProfile(TimeStampedModel):
    """ Model for the staff user profile
        allow users to login to the dashboard
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE
    )
    staff_id = models.CharField(
        unique=True, max_length=9, validators=[MinLengthValidator(9)])
    # account_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICE, default="technical_staff")
    # email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11)
    region = models.ForeignKey("location.Region", on_delete=models.PROTECT)
    csp = models.ForeignKey("location.Csp", on_delete=models.PROTECT, blank=True, null=True)
    active = models.BooleanField(default=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Staff User Profile"
        verbose_name_plural = "Staff User Profiles"
        ordering = ["-updated", ]

    @property
    def groups(self):
        return [group.name for group in self.user.groups.all()]

    @property
    def get_last_login(self):
        return self.user.last_login
        
    @property
    def user_type(self):
        return "staff"

    @property
    def is_staff(self):
        return self.user.is_staff
        
    @property
    def is_superuser(self):
        return self.user.is_superuser
        
    @property
    def first_name(self):
        return f"{self.user.first_name}"

    @property
    def last_name(self):
        return f"{self.user.last_name}"

    @property
    def fullname(self):
        return f"{self.user.get_full_name()}"

    @property
    def username(self):
        return f"{self.user.username}"

    @property
    def last_login(self):
        return f"{self.user.u.last_login}"

    def get_email(self):
        # if self.email:
        #     return self.email
        return self.user.email

    def user_apps_privileges(self):
        dta = [p.get_form_format() for p in self.app_privileges.all()]

        return dta

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def region_title(self):
        return f"{self.region}"

    def csp_title(self):
        return f"{self.csp}"

    def __str__(self):
        return f"{self.fullname}"


class UserType(TimeStampedModel):
    """Model for Tracking User Type

    Args:
        TimeStampedModel ([timestamp, updated]): [Creation, Modification Timestamp]

    Returns:
        [Object]: [Django Model Object Instance of UserType]
    """
    title = models.CharField(max_length=50)
    uid = models.UUIDField(default=LongUniqueId, unique=True)
    status = models.BooleanField(default=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "User Type"
        verbose_name_plural = "User Types"
        ordering = ["-updated", "title"]

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".capitalize()
        super(UserType, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"


class VendorProfile(TimeStampedModel):
    """ Model for the Vendor user profile
        allow users to login to the dashboard
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="vendor", on_delete=models.CASCADE
    )
    # email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11)
    vendor = models.ForeignKey("apps.Vendor", on_delete=models.CASCADE, related_name="staffs")
    active = models.BooleanField(default=False)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Vendor User Profile"
        verbose_name_plural = "Vendors Users Profiles"
        ordering = ["-updated", ]

    @property
    def groups(self):
        return [group.name for group in self.user.groups.all()]

    @property
    def get_last_login(self):
        return self.user.last_login
        
    @property
    def user_type(self):
        return "vendor"

    @property
    def first_name(self):
        return f"{self.user.first_name}"

    @property
    def last_name(self):
        return f"{self.user.last_name}"

    @property
    def fullname(self):
        return f"{self.user.get_full_name()}"

    @property
    def username(self):
        return f"{self.user.username}"

    @property
    def last_login(self):
        return f"{self.user.u.last_login}"

    def get_email(self):
        # if self.email:
        #     return self.email
        return self.user.email

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def vendor_title(self):
        return f"{self.vendor}"

    def __str__(self):
        return f"{self.fullname}"


class CustomerProfile(TimeStampedModel):
    """ Model for the customer user profile
        allow users to login to the dashboard
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="customer", on_delete=models.CASCADE
    )
    # email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=11)
    region = models.ForeignKey("location.Region", on_delete=models.PROTECT, blank=True, null=True)
    address = models.CharField(max_length=150)
    active = models.BooleanField(default=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"
        ordering = ["-updated", ]

    @property
    def groups(self):
        return [group.name for group in self.user.groups.all()]

    @property
    def get_last_login(self):
        return self.user.last_login
        
    @property
    def user_type(self):
        return "customer"

    @property
    def first_name(self):
        return f"{self.user.first_name}"

    @property
    def last_name(self):
        return f"{self.user.last_name}"

    @property
    def fullname(self):
        return f"{self.user.get_full_name()}"

    @property
    def username(self):
        return f"{self.user.username}"

    @property
    def last_login(self):
        return f"{self.user.u.last_login}"

    @property
    def get_email(self):
        # if self.email:
        #     return self.email
        return self.user.email

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def region_title(self):
        return f"{self.region}"
        
    def __str__(self):
        return f"{self.fullname}"


def is_valid_nimsa(nimsa_number):
    pattern = r"CC/CEIF/PR/\d{4,5}"
    # if re.match("CC/CEF/PR/[0-9]{4,5}", nimsa_number):
    if re.match(pattern, nimsa_number):
        return True
    else:
        return False
        


def validate_contractor_nimsa(value):
    if is_valid_nimsa(value):
        print(f"Val: {value}")
        return value
    else:
        raise ValidationError("Invalid NIMSA Number !!!")



class ContractorProfile(TimeStampedModel):
    """ Model for the Contractor user profile
        allow users to login to the dashboard
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="contractor", on_delete=models.CASCADE
    )
    uid = models.CharField(max_length=10, default=genserial)
    # email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11)
    company_name = models.CharField(max_length=255)
    nemsa_licence = models.CharField(
        unique=True, max_length=16, validators=[MinLengthValidator(14), validate_contractor_nimsa])
    licence_expire_date = models.DateField()
    address = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Contractor User Profile"
        verbose_name_plural = "Contractors Users Profiles"
        ordering = ["-updated", ]

    @property
    def groups(self):
        return [group.name for group in self.user.groups.all()]

    @property
    def get_last_login(self):
        return self.user.last_login

    @property
    def user_type(self):
        return "contractor"

    @property
    def first_name(self):
        return f"{self.user.first_name}"

    @property
    def last_name(self):
        return f"{self.user.last_name}"

    @property
    def fullname(self):
        return f"{self.user.get_full_name()}"

    @property
    def username(self):
        return f"{self.user.username}"

    @property
    def last_login(self):
        return f"{self.user.u.last_login}"

    def get_email(self):
        return self.user.email

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()

    def __str__(self):
        return f"{self.fullname}"


def dlt_expired():
    return timezone.now() + timezone.timedelta(days = 1)

class PasswordResetTokens(TimeStampedModel):
    """ 
        Model for the storing Password Reset Tokens
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="password_reset_tokens", on_delete=models.CASCADE
    )
    token = models.CharField(max_length=10, default=genserial, unique=True)
    expired_time = models.DateTimeField(default=dlt_expired)
    active = models.BooleanField(default=True)
    sent_count = models.PositiveIntegerField(default=0)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "Password Reset Token"
        verbose_name_plural = "Passwords Reset Tokens"
        ordering = ("-updated", )
        # unique_together = ("user", "active",)

    @property
    def first_name(self):
        return f"{self.user.first_name}"

    @property
    def last_name(self):
        return f"{self.user.last_name}"

    @property
    def fullname(self):
        return f"{self.user.get_full_name()}"

    @property
    def username(self):
        return f"{self.user.username}"

    @property
    def last_login(self):
        return f"{self.user.u.last_login}"

    def get_email(self):
        return self.user.email

    def audits(self):
        dta = self.history.all().order_by('-history_date')[:2].values()
        return dta

    def revisions(self):
        return self.history.count()
        
    def get_expired(self):
        now = timezone.now()
        if now > self.expired_time:
            expired_time = "Expired"
        else:
            expired_time = self.expired_time
        # obj.starts += timedelta(days=1, hours=2)
        return expired_time
        
    def email_user(self):
        subject = "CENTRAL PASSWORD RESET | KEDCO"
        signature = "System Development and Support Unit of KEDCO ICT (SDS)"
        html_message = render_to_string(
            template_name="core/accounts/password_reset_mail_template.html", 
            context={
                "subject": subject,
                "details": self,
                "signature": signature,
            }
        )
        msg = strip_tags(html_message)

        try:
            status = send_mail(
                subject=subject,
                message=msg,
                html_message=html_message,
                from_email=settings.SERVER_EMAIL,
                recipient_list=[f"{self.user.email}",],
                fail_silently=False,
            )
            self.sent_count += 1
            self.save()
        except Exception as exp:
            print(exp)
            status = 0
        return status

    def __str__(self):
        return f"{self.fullname}"
