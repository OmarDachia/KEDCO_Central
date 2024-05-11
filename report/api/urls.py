from django.urls import path
from .views import (
    # accounts
    UserStatistics,

    # meters
    MeterApplicationStatistics,
    
    #
    NMMPMeterStatistics,
    #
    VendorStatistics,
    
   
)

urlpatterns = [
    path("user/stats/", UserStatistics.as_view()),
    #
    path("meters/stats/", MeterApplicationStatistics.as_view()),
    #
    path("nmmp/stats/", NMMPMeterStatistics.as_view()),
    #
    path("vendor/stats/", VendorStatistics.as_view()),
    
]
