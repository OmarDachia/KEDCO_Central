from django.urls import path
from .views import (
    ApplicationListAPIView,
    ApplicationDetailsAPIView,
    ApplicationSearchAPIView,
    UserAppPrivilegeUpdateAPIView,
    UserAppPrivilegeListAPIView,
    UserAppPrivilegeDetailsAPIView,
    UserAppPrivilegeHistoryAPIView,
    UserAppPrivilegeSearchAPIView,
    VendorListAPIView,
    VendorSearchAPIView,
    VendorDetailsAPIView,
)

urlpatterns = [
    path("application/list/", ApplicationListAPIView.as_view()),
    path("application/details/<pk>/", ApplicationDetailsAPIView.as_view()),
    path("application/search/", ApplicationSearchAPIView.as_view()),
    # path("application/delete/<pk>/", UserProfileDeleteAPIView.as_view()),

    path("app-privilege/update/<pk>/", UserAppPrivilegeUpdateAPIView.as_view()),
    path("app-privilege/list/", UserAppPrivilegeListAPIView.as_view()),
    path("app-privilege/details/<pk>/", UserAppPrivilegeDetailsAPIView.as_view()),
    path("app-privilege/history/<pk>/", UserAppPrivilegeHistoryAPIView.as_view()),
    path("app-privilege/search/", UserAppPrivilegeSearchAPIView.as_view()),
    # path("app-privilege/delete/<pk>/", UserProfileDeleteAPIView.as_view()),
    path("vendor/list/", VendorListAPIView.as_view()),
    path("vendor/search/", VendorSearchAPIView.as_view()),
    path("vendor/details/<pk>/", VendorDetailsAPIView.as_view()),
    # path("Vendor/delete/<pk>/", UserProfileDeleteAPIView.as_view()),
]
