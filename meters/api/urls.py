from django.urls import path
from .views import (
    MeterApplicationCreateAPIView,
    MeterApplicationListAPIView,
    MeterApplicationListAPIViewV2,
    MeterApplicationSearchAPIView,
    MeterApplicationDetailsAPIView,
    MeterApplicationUpdateAPIView,
    MeterApplicationDeleteAPIView,
    ##
    MeterApplicationKYCCreateAPIView,
    MeterApplicationKYCListAPIView,
    MeterApplicationKYCSearchAPIView,
    MeterApplicationKYCDetailsAPIView,
    MeterApplicationKYCUpdateAPIView,
    MeterApplicationKYCDeleteAPIView,
    ##
    MeterApplicationInstallationCreateAPIView,
    MeterApplicationInstallationListAPIView,
    MeterApplicationInstallationSearchAPIView,
    MeterApplicationInstallationDetailsAPIView,
    MeterApplicationInstallationUpdateAPIView,
    MeterApplicationInstallationDeleteAPIView,
    ##
    MeterPhaseListAPIView,
    ##
    MeterApplicationPaymentCreateAPIView,
    MeterApplicationPaymentListAPIView,
    MeterApplicationPaymentSearchAPIView,
    MeterApplicationPaymentDetailsAPIView,
    MeterApplicationPaymentUpdateAPIView,
    MeterApplicationPaymentDeleteAPIView,
    #
    ECMICaptureListAPIView,
    MAPUpfrontPARListAPIView,
    MAPUpfrontPARListVendorSpecificAPIView,
)

urlpatterns = [
    path("meter/application/create/", MeterApplicationCreateAPIView.as_view()),
    path("meter/application/list/", MeterApplicationListAPIView.as_view()),
    path("meter/application/list/v2/", MeterApplicationListAPIViewV2.as_view()),
    path("meter/application/search/", MeterApplicationSearchAPIView.as_view()),
    path("meter/application/details/<pk>/", MeterApplicationDetailsAPIView.as_view()),
    path("meter/application/update/<pk>/", MeterApplicationUpdateAPIView.as_view()),
    path("meter/application/delete/<pk>/", MeterApplicationDeleteAPIView.as_view()),
    
    ##
    path("meter/application/kyc/create/", MeterApplicationKYCCreateAPIView.as_view()),
    path("meter/application/kyc/list/", MeterApplicationKYCListAPIView.as_view()),
    path("meter/application/kyc/search/", MeterApplicationKYCSearchAPIView.as_view()),
    path("meter/application/kyc/details/<pk>/", MeterApplicationKYCDetailsAPIView.as_view()),
    path("meter/application/kyc/update/<pk>/", MeterApplicationKYCUpdateAPIView.as_view()),
    path("meter/application/kyc/delete/<pk>/", MeterApplicationKYCDeleteAPIView.as_view()),
    ##
    path("meter/application/installation/create/",
        MeterApplicationInstallationCreateAPIView.as_view()
    ),
    path("meter/application/installation/list/",
        MeterApplicationInstallationListAPIView.as_view()
    ),
    path("meter/application/installation/search/",
        MeterApplicationInstallationSearchAPIView.as_view()
    ),
    path("meter/application/installation/details/<pk>/",
        MeterApplicationInstallationDetailsAPIView.as_view()
    ),
    path("meter/application/installation/update/<pk>/",
        MeterApplicationInstallationUpdateAPIView.as_view()
    ),
    path("meter/application/installation/delete/<pk>/",
        MeterApplicationInstallationDeleteAPIView.as_view()
    ),
    
    ##
    path("meter/phase/list/", MeterPhaseListAPIView.as_view()),
    ##
    path("meter/application/payment/create/", MeterApplicationPaymentCreateAPIView.as_view() ),
    path("meter/application/payment/list/", MeterApplicationPaymentListAPIView.as_view() ),
    path("meter/application/payment/search/", MeterApplicationPaymentSearchAPIView.as_view() ),
    path("meter/application/payment/details/<pk>/", MeterApplicationPaymentDetailsAPIView.as_view() ),
    path("meter/application/payment/update/<pk>/", MeterApplicationPaymentUpdateAPIView.as_view() ),
    path("meter/application/payment/delete/<pk>/", MeterApplicationPaymentDeleteAPIView.as_view() ),
    ##
    path("meter/application/ecmi-capture/list/",
        ECMICaptureListAPIView.as_view()
    ),
    path("meter/application/map-upfront/list/",
        MAPUpfrontPARListAPIView.as_view()
    ),
    path("meter/application/vendor-map-upfront/list/",
        MAPUpfrontPARListVendorSpecificAPIView.as_view()
    ),

]
