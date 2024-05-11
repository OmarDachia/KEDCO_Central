from django.urls import path
from .views import (
    NMMPKYCCreateAPIView,
    NMMPKYCListAPIView,
    NMMPKYCSearchAPIView,
    NMMPKYCDetailsAPIView,
    NMMPKYCUpdateAPIView,
    NMMPKYCDeleteAPIView,
    #
    AssignMeter,
    #
    NMMPMeterUploadAPIView,
    NMMPMeterCreateAPIView,
    NMMPMeterListAPIView,
    NMMPMeterSearchAPIView,
    NMMPMeterDetailsAPIView,
    NMMPMeterUpdateAPIView,
    NMMPMeterDeleteAPIView,
    #
    NMMPMeterInstallationCreateAPIView,
    NMMPMeterInstallationListAPIView,
    NMMPMeterInstallationSearchAPIView,
    NMMPMeterInstallationDetailsAPIView,
    NMMPMeterInstallationUpdateAPIView,
    NMMPMeterInstallationDeleteAPIView,
    #
    NMMPECMICaptureListAPIView,
    NMMPARListAPIView,
    NMMPVendorInstallationListAPIView,
    #
    NMMPApplicationTypeCreateAPIView,
    NMMPApplicationTypeListAPIView,
    NMMPApplicationTypeSearchAPIView,
    NMMPApplicationTypeDetailsAPIView,
    NMMPApplicationTypeUpdateAPIView,
    NMMPApplicationTypeDeleteAPIView,
   
)

urlpatterns = [
    path("kyc/create/", NMMPKYCCreateAPIView.as_view()),
    path("kyc/list/", NMMPKYCListAPIView.as_view()),
    path("kyc/search/", NMMPKYCSearchAPIView.as_view()),
    path("kyc/details/<pk>/", NMMPKYCDetailsAPIView.as_view()),
    path("kyc/update/<pk>/", NMMPKYCUpdateAPIView.as_view()),
    # path("kyc/delete/<pk>/", NMMPKYCDeleteAPIView.as_view()),
    ##
    path("assign-meter/", AssignMeter.as_view()),
    ##
    path("meter/upload/", NMMPMeterUploadAPIView.as_view()),
    path("meter/create/", NMMPMeterCreateAPIView.as_view()),
    path("meter/list/", NMMPMeterListAPIView.as_view()),
    path("meter/search/", NMMPMeterSearchAPIView.as_view()),
    path("meter/details/<pk>/", NMMPMeterDetailsAPIView.as_view()),
    path("meter/update/<pk>/", NMMPMeterUpdateAPIView.as_view()),
    # path("meter/delete/<pk>/", NMMPMeterDeleteAPIView.as_view()),
    ##
    path("meter/installation/create/",
        NMMPMeterInstallationCreateAPIView.as_view()
    ),
    path("meter/installation/list/",
        NMMPMeterInstallationListAPIView.as_view()
    ),
    path("meter/installation/search/",
        NMMPMeterInstallationSearchAPIView.as_view()
    ),
    path("meter/installation/details/<pk>/",
        NMMPMeterInstallationDetailsAPIView.as_view()
    ),
    path("meter/installation/update/<pk>/",
        NMMPMeterInstallationUpdateAPIView.as_view()
    ),
    # path("meter/installation/delete/<pk>/",
    #     NMMPMeterInstallationDeleteAPIView.as_view()
    # ),
    #
    path("meter/ecmi-capture/list/",
        NMMPECMICaptureListAPIView.as_view()
    ),
    path("meter/ar/list/",
        NMMPARListAPIView.as_view()
    ),
    path("meter/vendor-installation/list/",
         NMMPVendorInstallationListAPIView.as_view()
    ),
    ##
    path("app-type/create/", NMMPApplicationTypeCreateAPIView.as_view()),
    path("app-type/list/", NMMPApplicationTypeListAPIView.as_view()),
    path("app-type/search/", NMMPApplicationTypeSearchAPIView.as_view()),
    path("app-type/details/<pk>/", NMMPApplicationTypeDetailsAPIView.as_view()),
    path("app-type/update/<pk>/", NMMPApplicationTypeUpdateAPIView.as_view()),
    path("app-type/delete/<pk>/", NMMPApplicationTypeDeleteAPIView.as_view()),
    ##
    
    
    
    
    
    
]
