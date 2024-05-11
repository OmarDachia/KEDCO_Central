from django.db import models
from core.abstract_models import TimeStampedModel
from simple_history.models import HistoricalRecords

# from audit.registry import audit


class LGA(TimeStampedModel):
    title = models.CharField(max_length=50)
    LGA_ID = models.CharField(max_length=10, blank=True, null=True)
    state = models.ForeignKey("State", on_delete=models.CASCADE, related_name="lgas")
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "LGA"
        verbose_name_plural = "LGAs"
        ordering = ["title", "state"]

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".capitalize()
        super(LGA, self).save(*args, **kwargs)

    def state_title(self):
        return f"{self.state.title}"

    def __str__(self):
        return self.title


class State(TimeStampedModel):
    title = models.CharField(max_length=50)
    State_ID = models.CharField(max_length=10)
    state_code = models.CharField(max_length=10)
    zone = models.CharField(max_length=50)
    zone_code = models.CharField(max_length=10)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        ordering = ["title", ]

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".capitalize()
        super(State, self).save(*args, **kwargs)

    def lgas_count(self):
        return self.lgas.all().count()

    def get_lgas(self):
        dta = self.lgas.all().values("pk", "title")
        return dta


    def __str__(self):
        return self.title


class Region(TimeStampedModel):
    title = models.CharField(max_length=50)
    state = models.ForeignKey("State", on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    cavti_id = models.PositiveIntegerField(blank=True, null=True)
    billing_prepaid_id = models.CharField(max_length=5, blank=True, null=True)
    billing_postpaid_id = models.CharField(max_length=5, blank=True, null=True)
    history = HistoricalRecords(bases=[TimeStampedModel])
    

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
        ordering = ["title", ]

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".capitalize()
        super(Region, self).save(*args, **kwargs)

    def state_title(self):
        return f"{self.state.title}"

    def __str__(self):
        return self.title


class Csp(TimeStampedModel):
    title = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey("Region", on_delete=models.PROTECT)
    lga = models.ForeignKey("LGA", on_delete=models.PROTECT, blank=True, null=True)
    address = models.CharField(max_length=150)
    cavti_id = models.PositiveIntegerField(blank=True, null=True)
    billing_prepaid_id = models.CharField(max_length=5, blank=True, null=True)
    billing_postpaid_id = models.CharField(max_length=5, blank=True, null=True)
    history = HistoricalRecords(bases=[TimeStampedModel])

    class Meta:
        verbose_name = "CSP"
        verbose_name_plural = "CSPs"
        ordering = ["title", ]

    def save(self, *args, **kwargs):
        self.title = f"{self.title}".upper()
        super(Csp, self).save(*args, **kwargs)

    def region_title(self):
        return f"{self.region.state.title}"

    def __str__(self):
        return self.title

# Register Models for Logging
# audit.register(LGA)
# audit.register(State)
