from django.urls import path
from .views import (
    StateList,
    StateComboList,
    StateDetailsAPIView,
    StateUpdateAPIView,
    StateDeleteAPIView,
    LGACreateAPIView,
    LGAListAPIView,
    LGADetailsAPIView,
    LGAUpdateAPIView,
    LGADeleteAPIView,
    ##
    RegionCreateAPIView,
    RegionListAPIView,
    RegionDetailsAPIView,
    RegionUpdateAPIView,
    RegionDeleteAPIView,
    CspCreateAPIView,
    CspListAPIView,
    CspDetailsAPIView,
    CspUpdateAPIView,
    CspDeleteAPIView,
)


urlpatterns = [
    path("state/list/", StateList.as_view()),
    path("state/list/combo/", StateComboList.as_view()),
    path("state/details/<pk>/", StateDetailsAPIView.as_view()),
    path("state/update/<pk>/", StateUpdateAPIView.as_view()),
    path("state/delete/<pk>/", StateDeleteAPIView.as_view()),
    path("lga/create/", LGACreateAPIView.as_view()),
    path("lga/list/", LGAListAPIView.as_view()),
    path("lga/details/<pk>/", LGADetailsAPIView.as_view()),
    path("lga/update/<pk>/", LGAUpdateAPIView.as_view()),
    path("lga/delete/<pk>/", LGADeleteAPIView.as_view()),
    ##
    path("region/create/", RegionCreateAPIView.as_view()),
    path("region/list/", RegionListAPIView.as_view()),
    path("region/details/<pk>/", RegionDetailsAPIView.as_view()),
    path("region/update/<pk>/", RegionUpdateAPIView.as_view()),
    path("region/delete/<pk>/", RegionDeleteAPIView.as_view()),
    path("csp/create/", CspCreateAPIView.as_view()),
    path("csp/list/", CspListAPIView.as_view()),
    path("csp/details/<pk>/", CspDetailsAPIView.as_view()),
    path("csp/update/<pk>/", CspUpdateAPIView.as_view()),
    path("csp/delete/<pk>/", CspDeleteAPIView.as_view()),

]
